一份代码的n种看法 
下面的原始代码经过ai处理后,层级分明，总体俯瞰也方便，能极大地降低你的心智负担
<img width="1916" height="316" alt="image" src="https://github.com/user-attachments/assets/cba81ae5-179c-4741-af2d-79e4ce5d459a" />

<img width="1916" height="1012" alt="image" src="https://github.com/user-attachments/assets/8c37b5eb-2fea-40e9-9cc6-e6795253683e" />
原生代码
<img width="1916" height="1012" alt="image" src="https://github.com/user-attachments/assets/6dd257c6-6a7c-4f5e-9414-d83c9955fc3e" />

/* WiFi station Example
   This example code is in the Public Domain (or CC0 licensed, at your option.)
   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

#include <string.h>
#include <arpa/inet.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "nvs_flash.h"
#include "lwip/err.h"
#include "lwip/sys.h"
#include "lwip/sockets.h"
#include "lwip/netdb.h"

#define EXAMPLE_ESP_WIFI_SSID      "myap"
#define EXAMPLE_ESP_WIFI_PASS      "myappass"
#define EXAMPLE_ESP_MAXIMUM_RETRY  CONFIG_ESP_MAXIMUM_RETRY

// ... (保持原有的配置宏不变) ...

/* FreeRTOS event group to signal when we are connected */
static EventGroupHandle_t s_wifi_event_group;

#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT      BIT1

static const char *TAG = "wifi_station";
static int s_retry_num = 0;

/* ==================== IPv6 相关函数 ==================== */

// 打印所有 IPv6 地址（ESP-IDF v5.5 兼容版本）
static void print_all_ipv6_addresses(void)
{
    esp_netif_t *netif = esp_netif_get_handle_from_ifkey("WIFI_STA_DEF");
    if (netif == NULL) {
        ESP_LOGI(TAG, "No network interface found");
        return;
    }
    
    // v5.5 中 esp_netif_get_all_ip6 只需要2个参数
    esp_ip6_addr_t ip6_addr[5];
    int addr_count = esp_netif_get_all_ip6(netif, ip6_addr);
    
    if (addr_count == 0) {
        ESP_LOGI(TAG, "No IPv6 addresses found yet");
        return;
    }
    
    ESP_LOGI(TAG, "=== Found %d IPv6 address(es) ===", addr_count);
    for (int i = 0; i < addr_count && i < 5; i++) {
        char ip6_str[40];
        inet_ntop(AF_INET6, &ip6_addr[i], ip6_str, sizeof(ip6_str));
        
        // 判断地址类型（fe80::/10 是链路本地地址）
        if ((ip6_addr[i].addr[0] & 0xffc00000) == 0xfe800000) {
            ESP_LOGI(TAG, "IPv6[%d]: %s (Link Local)", i, ip6_str);
        } else {
            ESP_LOGI(TAG, "IPv6[%d]: %s (Global/Unique)", i, ip6_str);
        }
    }
}

// 强制启用 IPv6（ESP-IDF v5.5 兼容版本）
static void force_enable_ipv6(void)
{
    esp_netif_t *netif = esp_netif_get_handle_from_ifkey("WIFI_STA_DEF");
    if (netif != NULL) {
        // v5.5 中直接创建 IPv6 链路本地地址
        esp_err_t err = esp_netif_create_ip6_linklocal(netif);
        if (err == ESP_OK) {
            ESP_LOGI(TAG, "IPv6 link-local creation initiated");
        } else {
            ESP_LOGE(TAG, "IPv6 link-local creation failed: %s", esp_err_to_name(err));
        }
    }
}

// 获取并打印链路本地 IPv6 地址
static void print_link_local_ipv6(void)
{
    esp_netif_t *netif = esp_netif_get_handle_from_ifkey("WIFI_STA_DEF");
    if (netif == NULL) {
        return;
    }
    
    esp_ip6_addr_t ip6_addr;
    if (esp_netif_get_ip6_linklocal(netif, &ip6_addr) == ESP_OK) {
        char ip6_str[40];
        inet_ntop(AF_INET6, &ip6_addr, ip6_str, sizeof(ip6_str));
        ESP_LOGI(TAG, "Link-Local IPv6: %s", ip6_str);
    }
}

// IPv6 监控任务（每5秒打印一次）
static void ipv6_monitor_task(void *pvParameters)
{
    int check_count = 0;
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(5000));
        check_count++;
        ESP_LOGI(TAG, "=== IPv6 Check #%d ===", check_count);
        print_link_local_ipv6();
        print_all_ipv6_addresses();
    }
}

/* ==================== WiFi 事件处理 ==================== */

static void event_handler(void* arg, esp_event_base_t event_base,
                          int32_t event_id, void* event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        ESP_LOGI(TAG, "WiFi started, connecting...");
        esp_wifi_connect();
    }
    else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        if (s_retry_num < EXAMPLE_ESP_MAXIMUM_RETRY) {
            esp_wifi_connect();
            s_retry_num++;
            ESP_LOGI(TAG, "retry to connect to the AP (%d/%d)", s_retry_num, EXAMPLE_ESP_MAXIMUM_RETRY);
        } else {
            xEventGroupSetBits(s_wifi_event_group, WIFI_FAIL_BIT);
            ESP_LOGI(TAG, "connect to the AP fail");
        }
    }
    else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
        
        ESP_LOGI(TAG, "=== IPv4 Address Info ===");
        ESP_LOGI(TAG, "got ip: " IPSTR, IP2STR(&event->ip_info.ip));
        ESP_LOGI(TAG, "Netmask: " IPSTR, IP2STR(&event->ip_info.netmask));
        ESP_LOGI(TAG, "Gateway: " IPSTR, IP2STR(&event->ip_info.gw));
        
        // WiFi 连接成功后，主动启用 IPv6
        ESP_LOGI(TAG, "Enabling IPv6...");
        force_enable_ipv6();
        
        // 等待3秒后第一次检查 IPv6
        vTaskDelay(pdMS_TO_TICKS(3000));
        print_link_local_ipv6();
        
        s_retry_num = 0;
        xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    }
#if CONFIG_LWIP_IPV6
    else if (event_base == IP_EVENT && event_id == IP_EVENT_GOT_IP6) {
        ip_event_got_ip6_t* event = (ip_event_got_ip6_t*) event_data;
        char ip6_str[40];
        inet_ntop(AF_INET6, &event->ip6_info.ip, ip6_str, sizeof(ip6_str));
        
        ESP_LOGI(TAG, "=== IPv6 Event Triggered ===");
        ESP_LOGI(TAG, "IPv6 Address: %s", ip6_str);
        if ((event->ip6_info.ip.addr[0] & 0xffc00000) == 0xfe800000) {
            ESP_LOGI(TAG, "Address Type: Link Local");
        } else {
            ESP_LOGI(TAG, "Address Type: Other (Global/Unique)");
        }
    }
#endif
}

/* ==================== WiFi 初始化 ==================== */

void wifi_init_sta(void)
{
    s_wifi_event_group = xEventGroupCreate();
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();
    
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    
    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL, &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL, &instance_got_ip));
#if CONFIG_LWIP_IPV6
    esp_event_handler_instance_t instance_got_ip6;
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_GOT_IP6, &event_handler, NULL, &instance_got_ip6));
#endif
    
    wifi_config_t wifi_config = {
        .sta = {
            .ssid = EXAMPLE_ESP_WIFI_SSID,
            .password = EXAMPLE_ESP_WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };
    
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
    
    ESP_LOGI(TAG, "wifi_init_sta finished.");
    
    EventBits_t bits = xEventGroupWaitBits(s_wifi_event_group, WIFI_CONNECTED_BIT | WIFI_FAIL_BIT, pdFALSE, pdFALSE, portMAX_DELAY);
    
    if (bits & WIFI_CONNECTED_BIT) {
        ESP_LOGI(TAG, "connected to ap SSID:%s", EXAMPLE_ESP_WIFI_SSID);
    } else if (bits & WIFI_FAIL_BIT) {
        ESP_LOGI(TAG, "Failed to connect to SSID:%s", EXAMPLE_ESP_WIFI_SSID);
    }
}

/* ==================== 主函数 ==================== */

void app_main(void)
{
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    
    if (CONFIG_LOG_MAXIMUM_LEVEL > CONFIG_LOG_DEFAULT_LEVEL) {
        esp_log_level_set("wifi", CONFIG_LOG_MAXIMUM_LEVEL);
    }
    
    ESP_LOGI(TAG, "ESP_WIFI_MODE_STA");
    wifi_init_sta();
    
    // 启动 IPv6 监控任务
    xTaskCreate(ipv6_monitor_task, "ipv6_monitor", 4096, NULL, 5, NULL);
}
