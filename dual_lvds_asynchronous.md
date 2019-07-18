http://www.lisatech.cn/news/news.html&a=detail&id=2394
1 简介

　　本文主要介绍了 RockChip(以下简称 RK) SDK 平台上支持的异显方案，包括系统 API、补丁、内核配置方法等，适用于以下 SDK 平台：

　　l RK3188 Android4.4

　　l RK3188 Android5.1

　　l RK3288 Android4.4

　　l RK3288 Android5.1

　　2 系统 API

　　RK 双屏异显方案有两种方式：Android Presentation 和 RK dualscreen。Android Presentation 是 Google 提供的双屏方案，实现了 View 级别的 VOP 派发，逻辑均在同一个 APP 上进行控制;RK dualscreen 则是实现了 APP 级别的 VOP 派发，异显的两部分分别是不同的 APP。

　　Presentation 比较适用于对自身需求进行深入定制的方案，RK dualscreen 在满足深入定制方案下，也支持，快速集成多方 APP，进行功能整合。两者各有优缺点，也能够进行互补。

　　2.1 Android Presentation

　　2.1.1 API 介绍

　　官方 API 以及示例说明文档：

　　https://developer.android.com/reference/android/app/Presentation.html

　　Presentation 是 google 官方提供的一个特殊的 dialog 类型，用来将特定内容显示到其他非

　　主屏显示器上。它在创建时，需要绑定显示屏，并根据这个目标显示屏以及其大小来配置 context

　　和 resource。目前系统提供了两种方式来与目标显示屏进行绑定。

　　1. 通过 MediaRouter 接口获取并绑定：

　　MediaRouter mediaRouter =(MediaRouter)

　　context.getSystemService(Context.MEDIA_ROUTER_SERVICE); MediaRouter.RouteInfo route = mediaRouter.getSelectedRoute(); if(route !=null){

　　Display presentationDisplay = route.getPresentationDisplay();

　　if(presentationDisplay !=null){

　　Presentation presentation =newMyPresentation(context, presentationDisplay);

　　presentation.show();

　　}

　　}

　　2. 通过 DisplayManager 接口获取并绑定：

　　DisplayManager displayManager =(DisplayManager) context.getSystemService(Context.DISPLAY_SERVICE); Display[] presentationDisplays =

　　displayManager.getDisplays(DisplayManager.DISPLAY_CATEGORY_PRESENTATION); if(presentationDisplays.length >0){

　　// If there is more than one suitable presentation display, then we could consider

　　// giving the user a choice. For this example, we simply choose the first display

　　// which is the one the system recommends as the preferred presentation display. Display display = presentationDisplays[0];

　　Presentation presentation =new MyPresentation(context, presentationDisplay); presentation.show();

　　}

　　MediaRouter 和 DisplayManager 接口不在此处详细介绍。

　　Presentation 的接口使用简单，功能明确，主要接口如下：

　　1. 构造接口

　　(1) Presentation(Context outerContext,Display display)

　　接口说明：

　　实例一个使用默认主题，绑定到目标 display 上的 Presentation 对象。

　　参数说明：

　　outerContext：application 的 context 对象;

　　display：要绑定的目标 display，可以通过上述介绍的 MediaRouter 和 DisplayManager

　　接口获取。

　　(2) Presentation(Context outerContext, Display display, int theme)

　　接口说明：

　　实例一个使用特定主题，并绑定到目标 display 上的 Presentation 对象。

　　参数说明：

　　outerContext：application 的 context 对象;

　　display：要绑定的目标 display，可通过上述介绍的 MediaRouter 和 DisplayManager 接

　　口获取;

　　theme：窗口使用的主题资源。

　　2. 方法接口

　　(1) Display getDisplay()

　　接口说明：

　　获取当前 presentation 显示所在的目标屏。

　　(2) Resources getResources()

　　接口说明：

　　获取用于当前 presentation 的 Resources 对象。

　　(3) void onDisplayChanged()

　　接口说明：

　　当 presentation 绑定的 display 发生变化(如大小、方向等)时，系统会回调此接口，并且系统将自动调用 cancel()接口，关闭此 presentation。

　　(4) void onDisplayRemoved()

　　接口说明：

　　当 presentation 绑定的 display 被移除时，系统会回调此接口，并在此之后，系统会自动调

　　用 cancel()接口，关闭此 presentation。

　　(5) void show()

　　接口说明：

　　用 于 显 示 此 presentation ， 如 果 显 示 设 备 无 法找 到 ， 调 用 此 接 口 ， 将 抛 出

　　WindowManager.InvalidDisplayException 异常。

　　(6) void onStart()

　　接口说明：

　　当此 presentation 启动后，会调用此接口，类似 activity 的 onStart。

　　(7) void onStop()

　　接口说明：

　　当此 presentation 正在走 stop 流程时，将会调用到此接口，类似 activity 的 onStop。

　　2.1.2 Presentation 示例

　　谷歌官方提供了 ApiDemo，用来展示各个 API 的使用，presentation 在源码中的范例路径

　　为：

　　development/samples/ApiDemos/./src/com/example/android/apis/app/Presentation Activity.java。

　　关键代码(红色字体)介绍如下：

　　1. 获取目标显示设备: public void updateContents() {

　　clear();

　　String displayCategory = getDisplayCategory();

　　Display[] displays = mDisplayManager.getDisplays(displayCategory); addAll(displays);

　　Log.d(TAG, "There are currently " + displays.length + " displays connected."); for (Display display : displays) {

　　Log.d(TAG, "" + display);

　　}

　　}

　　private String getDisplayCategory() {

　　return mShowAllDisplaysCheckbox.isChecked() ? null : DisplayManager.DISPLAY_CATEGORY_PRESENTATION;

　　}

　　通过 DisplayManager 接口获取 PRESENTATION 类型的显示设备，添加到队列当中并绑定

　　到各个 View 当中。

　　2. 点击 CheckItem，创建 Presentation，并显示：

　　public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) { if (buttonView == mShowAllDisplaysCheckbox) {

　　// Show all displays checkbox was toggled. mDisplayListAdapter.updateContents();

　　} else {

　　//Display item checkbox was toggled.

　　final Display display = (Display)buttonView.getTag();

　　if (isChecked) {

　　PresentationContents contents = new PresentationContents(getNextPhoto()); showPresentation(display, contents);

　　} else {

　　hidePresentation(display);

　　}

　　}

　　}

　　通过 View 的 setTag 绑定对象的方法，将 display 对象绑定到具体 View 当中，并在需要时，通过 getTag 获取对应的 display 对象。

　　private void showPresentation(Display display, PresentationContents contents) { final int displayId = display.getDisplayId();

　　if (mActivePresentations.get(displayId) != null) {

　　return;

　　}

　　Log.d(TAG, "Showing presentation photo #" + contents.photo + " on display #" + displayId +

　　".");

　　DemoPresentation presentation = new DemoPresentation(this, display, contents);

　　presentation.show();

　　presentation.setOnDismissListener(mOnDismissListener);

　　mActivePresentations.put(displayId, presentation);

　　}

　　在范例中自定义了一个 Presentation 类，此处通过调用自定义的 Presentation，并显式调

　　用 show 方法，将此 Presentation 显示到对应的 display 上。

　　此处的 PresentationContents 只是自定义了一个数据的封装方式，传给 Presentation，实

　　际使用当中，可以根据项目需要，或者通过其他方式给显示的数据即可，不需要也创建这类对象。

　　3. 自定义 Presentation 类：

　　private final class DemoPresentation extends Presentation { final PresentationContents mContents;

　　public DemoPresentation(Context context, Display display, PresentationContents contents) { super(context, display);

　　mContents = contents;

　　}

　　@Override

　　protected void onCreate(Bundle savedInstanceState) {

　　// Be sure to call the super class. super.onCreate(savedInstanceState);

　　// Get the resources for the context of the presentation.

　　// Notice that we are getting the resources from the context of the presentation.

　　Resources r = getContext().getResources();

　　// Inflate the layout. setContentView(R.layout.presentation_content); final Display display = getDisplay();

　　final int displayId = display.getDisplayId(); final int photo = mContents.photo;

　　// Show a caption to describe what‘s going on. TextView text = (TextView)findViewById(R.id.text); text.setText(r.getString(R.string.presentation_photo_text, photo, displayId,

　　display.getName()));

　　// Show a n image for visual interest.

　　ImageView image = (ImageView)findViewById(R.id.image); image.setImageDrawable(r.getDrawable(PHOTOS[photo]));

　　GradientDrawable drawable = new GradientDrawable(); drawable.setShape(GradientDrawable.RECTANGLE); drawable.setGradientType(GradientDrawable.RADIAL_GRADIENT);

　　// Set the background to a random gradient. Point p = new Point(); getDisplay().getSize(p); drawable.setGradientRadius(Math.max(p.x, p.y) / 2); drawable.setColors(mContents.colors);

　　findViewById(android.R.id.content).setBackground(drawable);

　　}

　　}

　　如上，可看出 Presentation 跟 Activity 的继承类似，在构造中调用父类构造方法，在 onCreate 中调用 setContentView 方法设置显示的 View 布局。

　　以上便是 Android Presentation 的大体介绍，总体上来说，使用比较容易，其是 Dialog 类

　　的子类，继承和使用与 activity 类似，比较重要的一个步骤是如何获取要绑定的 display 对象，

　　实现了 View 级别的 vop 派发。

　　2.2 RK DualScreen

　　RK DualScreen 主要区别与 android presentation，在于它实现了应用的派发，允许厂商快速根据现有的 app 功能，进行模块的集成，减少开发周期和研发成本。

　　2.2.1 API 介绍

　　以下新增 API 主要是在框架中的 Context 以及 Activity 类中添加，实际使用过程中要注意实

　　例的对象。

　　(1) public void setDualScreen(boolean enable) Context 类

　　接口说明：

　　此接口用来开启/关闭系统的双屏异显功能模块;

　　参数说明：

　　true：打开双屏异显功能;

　　false：关闭双屏异显功能。

　　注意：

　　由于此接口需要进行 update config，因此要求 app 需要集成如下：

　　l Permission：

　　AndroidManifest.xml：

　　l System share uid：

　　AndroidManifest.xml：

　　android:sharedUserId="android.uid.system"

　　Android.mk：

　　LOCAL_CERTIFICATE := platform

　　LOCAL_SDK_VERSION := current

　　(2) public void moveAppToDisplay(int id) Activity 类

　　接口说明：

　　用于将当前应用移动到指定的 display id 设备上，使用此接口，开发厂商需要做好副屏的 APP

　　管理，避免滞留太多的 APP 在副屏，导致出现一些性能或者管理混乱问题。

　　参数说明：

　　Id： 目标 display 的 id。

　　取值范围：当前系统包含的所有显示设备的 ID 值。

　　(3) public void syncDualDisplay() Activity 类

　　接口说明：

　　用于同步显示状态，将异显的状态同步回同显状态;

　　(4) public void moveExtendDisplay() Activity 类

　　接口说明：

　　此接口是 RK 内部框架集成在手势操作上的方法，与 moveAppToDisplay 接口的主要区别在

　　于，此接口流程上添加了将副屏上的应用个数控制在 1 个，即，当移动新的 APP 到副屏时，会将

　　副屏旧的 APP 移动至主屏。

　　2.2.2 RockChip DualScreen 接口使用示例

　　示例代码参见补丁中的 DemoRKDualScreenDemo.tar.gz 工程。该工程，主要演示的功

　　能为：获取 display 列表并显示，用户点击副屏(当前在主屏，因此点击主屏框架不做处理)id

　　后，应用调用接口显示到副屏，延迟 4s 后自动调用切换到主屏，延迟 4s 调用框架异显接口(带

　　app 个数控制)，延迟 4s 后会再调用同步接口，同步状态为同显。

　　关键代码见如下：

　　1. 打开双屏异显功能

　　public void openDualScreen(View view) {

　　mContext.setDualScreen(true);

　　}

　　2. 获取显示列表

　　public void updateContents() { clear();

　　Display[] displays = mDisplayManager.getDisplays(null); addAll(displays);

　　Log.d(TAG, "There are currently " + displays.length + " displays connected."); for (Display display : displays) {

　　Log.d(TAG, "" + display);

　　}

　　notifyDataSetChanged();

　　}

　　3. 点击 listview，调用接口将 app 派发到对应 display 设备上：

　　private final OnItemClickListener itemClickListener = new OnItemClickListener() { public void onItemClick(AdapterView parent, View view, int position, long id) {

　　int displayid = ((ViewHolder)view.getTag()).displayid;

　　Log.e(TAG, "click list position = " + position + ", displayId = "+ displayid); ((MainActivity)MainActivity.this).moveAppToDisplay(displayid); mHandler.sendEmptyMessageDelayed(MOVE_TO_DISPLAY_0, 4000);

　　}

　　};

　　4. 移动当前应用到主屏：

　　case MOVE_TO_DISPLAY_0:

　　Log.d(TAG, "MOVE BACK TO #0"); ((MainActivity)MainActivity.this).moveAppToDisplay(0); mTextView.setText("move to display:0"); mHandler.sendEmptyMessageDelayed(MOVE_EXTEND_DISPLAY, 4000); break;

　　主屏默认 ID 为 0,我们这里直接写 0,实际当中可以通过 Display 对象进行判断。

　　5. 移动当前应用到外部显示设备：

　　case MOVE_EXTEND_DISPLAY:

　　Log.d(TAG, "MOVE TO EXTEND DISPLAY");

　　((MainActivity)MainActivity.this).moveExtendDisplay();

　　mTextView.setText("move to display:EXTEND DISPLAY"); mHandler.sendEmptyMessageDelayed(SYNC_DUAL_SCREEN, 4000);

　　break;

　　此接口为 RK 框架集成的手势操作的接口，自带管理副屏应用，限制副屏应用个数为 1 个。

　　6. 将状态同步为同显状态：

　　case SYNC_DUAL_SCREEN:

　　Log.d(TAG, "SYNC BACK");

　　mTextView.setText("move to display:SYNC");

　　((MainActivity)MainActivity.this).syncDualDisplay();

　　break;

　　7. 关闭双屏异显功能：

　　public void closeDualScreen(View view) {

　　mContext.setDualScreen(false);

　　}

　　3 补丁与配置

　　3.1 Android

　　3.1.1 RK3288 Android 5.1

　　1. 基于最新 SDK 打上补丁 frameworks_base_dualscreen_api-last.patch。

　　2. 使 用 双 LCD 屏 时 ， 请 在 /hardware/rockchip/hwcomposer 打 上 补 丁

　　32885.1-hardware-rockchip-hwcomposer-base-on-c38e733b3.patch ， 并在 build.prop 里添加属性 ro.htg.force=1。

　　3.1.2 RK3288 Android 4.4

　　1. 单 LCD 屏加 HDMI，请用 repo 同步最新代码，然后依次打上 RK3288/4.4 目录下的两个补丁：

　　(1) fix_hwc_can‘t_be_patched_after_pull_source_code.7z

　　(2) [RK3288_Android4.4.4-SDK]双屏双显_Patch_V1.1.7z

　　2. 双 LCD 屏时，在 1)基础上，使用 hwcomposer_rga_force_htg.tar 替换工程中的源码目录 hardware/rk29/libhwcomposer。

　　3.1.3 RK3188 Android 5.1

　　1. 请基于最新 SDK 打上补丁 frameworks_base_dualscreen_api-last.patch。

　　2. SDK 默认支持 LCD + HDMI 双显场景。

　　3. 双 LCD 屏场景，请将 patch/rk3188/5.1/ hwcomposer.rk30board.so 替换工程中的 hwcomposer.rk30board.so，并在 build.prop 里添加属性 ro.htg.force=1。

　　3.1.4 RK3188 Android 4.4

　　打上补丁 RK3188/4.4/ RK3188_4.4_dual_screen.7z。

　　3.2 Kernel Driver

　　内核驱动根据安卓版本以及平台的不同会做区分。

　　3.2.1 RK3288 Android 5.1

　　1. rk3288 支持的显示接口可以任意组合。

　　2. 双屏异显时，一个显示接口当主屏，另一个当副屏;主副屏由板级 dts 文件确定，启动后无法动态更改;

　　3. 当两路显示接口显示不同分辨率时，rk3288 只能为一路显示接口提供精确时钟，另一路显示接口时钟会有微小频偏;

　　3.2.1.1 BOX 平台

　　1. 在 rk3288-box.dts 使能 lcdc0 和 lcdc1(默认关闭)，并确定主副屏顺序：

　　2. 将显示接口挂到对应的 lcdc，即不同显示接口连接的 lcdc_id 应不同。例如，HDMI 和CVBS(rk1000)会通过 dts 文件的配置来选择：

　　3. lcdc 模块上电顺序，默认 lcdc0 先加载。若需要修改，需调整 rk3288.dtsi 中 lcdc0 和 lcdc1 的顺序，放在前面的先加载。

　　3.2.1.2 MID 平台

　　1. 屏 + HDMI。SDK 默认支持方式。屏有 EDP，LVDS，MIPI 等接口，使用时在 dts 中

　　使能对应的接口，关闭其他没用到的接口。

　　2. 双 LCD 屏。该接法内核需打上补丁 RK3228/5.1/RK3288_dual_lcd.patch。

　　使用该补丁的注意事项：

　　(1) 默认接法为 LVDS + EDP，如果是 MIPI 屏请参考 EDP 屏驱动做修改;

　　(2) disp_mode 为 DUAL_LCD 模式，主要用于支持双 LCD 显示的产品配置;

　　l fb 节点中属性 rockchip,disp-mode 设置为 DUAL_LCD;

　　l rk_screen 节点打开两个 screen 节点配置，分别设置 sceen_prop 属性为 PRMRY

　　和 EXTEND 并 include 对应屏的时序配置文件。

　　l LCDC0 和 LCDC1 节点同时打开;

　　l 打开 EDP、MIPI、LVDS 中需要使用的两个节点，关闭不需要的其他设备节点，如

　　HDMI 和 MIPI;

　　l 设置 fb 节点中 rockchip,uboot-logo-on=<0>;

　　(3) 双 LCD 屏用法，HWC 也需要做相应的修改，请见章节 3.1.1。

　　3.2.2 RK3288 Android 4.4

　　4.4 的双屏异显功能只在 MID 平台上实现，接法为 LCD + HDMI，HDMI 作为副屏。

　　4 双屏触摸

　　4.1 原理说明

　　从原生的 Android 系统的代码中可以看到 , 触摸的事件实体中已经包含了一个叫做

　　displayId 的成员。这说明双触摸的框架 Android 基本已经做好，如果触摸事件的 displayId

　　对应的是主屏，那么它就会把该事件送给主屏的 TouchedWindow。同理，如果触摸事件的

　　displayId 对应的是副屏，那么它就会把该事件送给副屏的 TouchedWindow。所以关键的地方就是这个 displayId 是如何被赋值的， 查看 inputflinger 的 Eventhub.cpp 代码

　　openDeviceLocked 中，如果是 USB 或者蓝牙接口的触摸屏，该触摸设备会设置一个

　　INPUT_DEVICE_CLASS_EXTERNAL 属性，那么 input 框架就是根据这个属性来最终将其的

　　event 送给副屏的 TouchedWindow。

　　所以如果使用触摸屏，主屏使用的是 I2C 接口，副屏使用的是 USB 或者蓝牙接口。那么就可以实现双触摸。如果两个都使用的是 I2C，或者都使用的是 USB(蓝牙)，只要修改代码保证主屏上的触摸设备不带 INPUT_DEVICE_CLASS_EXTERNAL 属性，副屏上的触摸设备带上这个

　　属性，也可以实现双触摸功能。

　　4.2 补丁

　　在 framework/base 目录下打上 frameworks_base_dual-TouchInput-feature.patch。

　　注意：本补丁只适用于 Android Presentation 方案的双屏异显。
