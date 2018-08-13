// 08-07 13:52:03.528 10037  1994  1994 I sysui_multi_action: [757,803,799,DismissTextView,802,0]
//  isblank
#include <stdio.h>// while :; do a shell ifconfig wlan0|grep 'RX bytes'|tr ':' ' '|awk '{ print $3 }'|rev|split_3_field|rev;sleep 1;echo ' ';done
int getfield_pos(char *s, int n, int *pos){//n is input len + 1	
	int len = strlen(s);
	int fie=-1;	
	int i =0; int field = 0;	
	for(i=0;i<len; i++){
		while(i<len-2 && isblank(s[i])){
			i++;
		}
		if(!isblank(s[i]))
			fie++;
		if(fie == n){ *pos=i; return 0;
			break;}
		while(i<len-2 && !isblank(s[i])){
			i++;
		}	
	}
	return -1;
}
#define MAX_LEN 1024*100
int main(int argc,char *argv[]){
	// char buf[1024]={0};
	// while(fgets(buf, 1024, stdin)){
	// 	// printf("%s", buf);
	// 	int len=strlen(buf);//argv[1]);
	// 	char *t=buf;//argv[1];
	// 	int i;int j=1;
	// 	for(i=0;i<len-2; i++){
	// 		printf("%c", t[i]);
	// 		if(j++%3==0)
	// 			printf(",");
	// 	}
	// 	printf("%c", t[i]);
	// }
	int pos = 0;
	// char *s=" 08-07 13:52:03.528 10037  	1994  1994 I sysui_multi_action: [757,803,799,DismissTextView,802,0]";
	// int r = getfield_pos(s, 5, &pos);
	// printf(" %d str:%s\n", r, r?"":s+pos);
	if(argc != 3){
		printf(" %s filex filedxxx \n such as:\n %s filex 3 \n", argv[0], argv[0]);
		return -1;
	}
	int fie = atoi(argv[2]);
	FILE *pF = fopen(argv[1], "rb");
	if(pF){
		char s[MAX_LEN+1]={0};
		char *fgets(char *s, int size, FILE *stream);
		while(fgets(s, MAX_LEN, pF)){
			if(!getfield_pos(s, fie, &pos)){
				fprintf(stdout, "%s", s+pos);
			}
		}
		fclose(pF);
	}
}