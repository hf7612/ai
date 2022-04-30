 .     final class RemoteServiceException extends AndroidRuntimeException {
 . RemoteServiceException        public RemoteServiceException(String msg) {
 .     public final class ActivityThread extends ClientTransactionHandler {
 .         final ArrayList<Application> mAllApplications
 .         private static final class ProviderKey {
 . ProviderKey            public ProviderKey(String authority, int userId) {
 . equals            public boolean equals(Object o) {
 . hashCode            public int hashCode() {
 .         final ArrayMap<ProviderKey, ProviderClientRecord> mProviderMap
 .         final ArrayMap<IBinder, ProviderRefCount> mProviderRefCountMap
 .         final ArrayMap<IBinder, ProviderClientRecord> mLocalProviders
 .         final ArrayMap<ComponentName, ProviderClientRecord> mLocalProvidersByName
 .         final ArrayMap<Activity, ArrayList<OnActivityPausedListener>> mOnPauseListeners
 .         public static final class ActivityClientRecord {
 . ActivityClientRecord            public ActivityClientRecord() {
 . ActivityClientRecord            public ActivityClientRecord(IBinder token, Intent intent, int ident,                ActivityInfo info, Configuration overrideConfig, CompatibilityInfo compatInfo,                String referrer, IVoiceInteractor voiceInteractor, Bundle state,                PersistableBundle persistentState, List<ResultInfo> pendingResults,                List<ReferrerIntent> pendingNewIntents, boolean isForward,                ProfilerInfo profilerInfo, ClientTransactionHandler client,                IBinder assistToken) {
 . init            private void init() {
 . getLifecycleState            public int getLifecycleState() {
 . setState            public void setState(@LifecycleState int newLifecycleState) {
 . isPreHoneycomb            private boolean isPreHoneycomb() {
 . isPreP            private boolean isPreP() {
 . isPersistable            public boolean isPersistable() {
 . isVisibleFromServer            public boolean isVisibleFromServer() {
 . toString            public String toString() {
 . getStateString            public String getStateString() {
 .         final class ProviderClientRecord {
 .         static final class ReceiverData extends BroadcastReceiver.PendingResult {
 . ReceiverData            public ReceiverData(Intent intent, int resultCode, String resultData, Bundle resultExtras,                boolean ordered, boolean sticky, IBinder token, int sendingUser) {
 . toString            public String toString() {
 .         static final class CreateBackupAgentData {
 . toString            public String toString() {
 .         static final class CreateServiceData {
 . toString            public String toString() {
 .         static final class BindServiceData {
 . toString            public String toString() {
 .         static final class ServiceArgsData {
 . toString            public String toString() {
 .         static final class AppBindData {
 . toString            public String toString() {
 .         static final class Profiler {
 . setProfiler            public void setProfiler(ProfilerInfo profilerInfo) {
 . startProfiling            public void startProfiling() {
 . stopProfiling            public void stopProfiling() {
 .         static final class DumpComponentInfo {
 .         static final class ContextCleanupInfo {
 .         static final class DumpHeapData {
 .         static final class UpdateCompatibilityData {
 .         static final class RequestAssistContextExtras {
 .         private class ApplicationThread extends IApplicationThread.Stub {
 . scheduleSleeping            public final void scheduleSleeping(IBinder token, boolean sleeping) {
 . scheduleReceiver            public final void scheduleReceiver(Intent intent, ActivityInfo info,                CompatibilityInfo compatInfo, int resultCode, String data, Bundle extras,                boolean sync, int sendingUser, int processState) {
 . scheduleCreateBackupAgent            public final void scheduleCreateBackupAgent(ApplicationInfo app,                CompatibilityInfo compatInfo, int backupMode, int userId) {
 . scheduleDestroyBackupAgent            public final void scheduleDestroyBackupAgent(ApplicationInfo app,                CompatibilityInfo compatInfo, int userId) {
 . scheduleCreateService            public final void scheduleCreateService(IBinder token,                ServiceInfo info, CompatibilityInfo compatInfo, int processState) {
 . scheduleBindService            public final void scheduleBindService(IBinder token, Intent intent,                boolean rebind, int processState) {
 . scheduleUnbindService            public final void scheduleUnbindService(IBinder token, Intent intent) {
 . scheduleServiceArgs            public final void scheduleServiceArgs(IBinder token, ParceledListSlice args) {
 . scheduleStopService            public final void scheduleStopService(IBinder token) {
 . bindApplication            public final void bindApplication(String processName, ApplicationInfo appInfo,                List<ProviderInfo> providers, ComponentName instrumentationName,                ProfilerInfo profilerInfo, Bundle instrumentationArgs,                IInstrumentationWatcher instrumentationWatcher,                IUiAutomationConnection instrumentationUiConnection, int debugMode,                boolean enableBinderTracking, boolean trackAllocation,                boolean isRestrictedBackupMode, boolean persistent, Configuration config,                CompatibilityInfo compatInfo, Map services, Bundle coreSettings,                String buildSerial, AutofillOptions autofillOptions,                ContentCaptureOptions contentCaptureOptions, long[] disabledCompatChanges) {
 . runIsolatedEntryPoint            public final void runIsolatedEntryPoint(String entryPoint, String[] entryPointArgs) {
 . scheduleExit            public final void scheduleExit() {
 . scheduleSuicide            public final void scheduleSuicide() {
 . scheduleApplicationInfoChanged            public void scheduleApplicationInfoChanged(ApplicationInfo ai) {
 . updateTimeZone            public void updateTimeZone() {
 . clearDnsCache            public void clearDnsCache() {
 . updateHttpProxy            public void updateHttpProxy() {
 . processInBackground            public void processInBackground() {
 . dumpService            public void dumpService(ParcelFileDescriptor pfd, IBinder servicetoken, String[] args) {
 . scheduleRegisteredReceiver            public void scheduleRegisteredReceiver(IIntentReceiver receiver, Intent intent,                int resultCode, String dataStr, Bundle extras, boolean ordered,                boolean sticky, int sendingUser, int processState) throws RemoteException {
 . scheduleLowMemory            public void scheduleLowMemory() {
 . profilerControl            public void profilerControl(boolean start, ProfilerInfo profilerInfo, int profileType) {
 . dumpHeap            public void dumpHeap(boolean managed, boolean mallocInfo, boolean runGc, String path,                ParcelFileDescriptor fd, RemoteCallback finishCallback) {
 . attachAgent            public void attachAgent(String agent) {
 . attachStartupAgents            public void attachStartupAgents(String dataDir) {
 . setSchedulingGroup            public void setSchedulingGroup(int group) {
 . dispatchPackageBroadcast            public void dispatchPackageBroadcast(int cmd, String[] packages) {
 . scheduleCrash            public void scheduleCrash(String msg) {
 . dumpActivity            public void dumpActivity(ParcelFileDescriptor pfd, IBinder activitytoken,                String prefix, String[] args) {
 . dumpProvider            public void dumpProvider(ParcelFileDescriptor pfd, IBinder providertoken,                String[] args) {
 . dumpMemInfo            public void dumpMemInfo(ParcelFileDescriptor pfd, Debug.MemoryInfo mem, boolean checkin,                boolean dumpFullInfo, boolean dumpDalvik, boolean dumpSummaryOnly,                boolean dumpUnreachable, String[] args) {
 . dumpMemInfo            private void dumpMemInfo(PrintWriter pw, Debug.MemoryInfo memInfo, boolean checkin,                boolean dumpFullInfo, boolean dumpDalvik, boolean dumpSummaryOnly, boolean dumpUnreachable) {
 . dumpMemInfoProto            public void dumpMemInfoProto(ParcelFileDescriptor pfd, Debug.MemoryInfo mem,                boolean dumpFullInfo, boolean dumpDalvik, boolean dumpSummaryOnly,                boolean dumpUnreachable, String[] args) {
 . dumpMemInfo            private void dumpMemInfo(ProtoOutputStream proto, Debug.MemoryInfo memInfo,                boolean dumpFullInfo, boolean dumpDalvik,                boolean dumpSummaryOnly, boolean dumpUnreachable) {
 . dumpGfxInfo            public void dumpGfxInfo(ParcelFileDescriptor pfd, String[] args) {
 . getDatabasesDir            private File getDatabasesDir(Context context) {
 . dumpDatabaseInfo            private void dumpDatabaseInfo(ParcelFileDescriptor pfd, String[] args, boolean isSystem) {
 . dumpDbInfo            public void dumpDbInfo(final ParcelFileDescriptor pfd, final String[] args) {
 . run                        public void run() {
 . unstableProviderDied            public void unstableProviderDied(IBinder provider) {
 . requestAssistContextExtras            public void requestAssistContextExtras(IBinder activityToken, IBinder requestToken,                int requestType, int sessionId, int flags) {
 . setCoreSettings            public void setCoreSettings(Bundle coreSettings) {
 . updatePackageCompatibilityInfo            public void updatePackageCompatibilityInfo(String pkg, CompatibilityInfo info) {
 . scheduleTrimMemory            public void scheduleTrimMemory(int level) {
 . scheduleTranslucentConversionComplete            public void scheduleTranslucentConversionComplete(IBinder token, boolean drawComplete) {
 . scheduleOnNewActivityOptions            public void scheduleOnNewActivityOptions(IBinder token, Bundle options) {
 . setProcessState            public void setProcessState(int state) {
 . setNetworkBlockSeq            public void setNetworkBlockSeq(long procStateSeq) {
 . scheduleInstallProvider            public void scheduleInstallProvider(ProviderInfo provider) {
 . updateTimePrefs            public final void updateTimePrefs(int timeFormatPreference) {
 . scheduleEnterAnimationComplete            public void scheduleEnterAnimationComplete(IBinder token) {
 . notifyCleartextNetwork            public void notifyCleartextNetwork(byte[] firstPacket) {
 . startBinderTracking            public void startBinderTracking() {
 . stopBinderTrackingAndDump            public void stopBinderTrackingAndDump(ParcelFileDescriptor pfd) {
 . scheduleLocalVoiceInteractionStarted            public void scheduleLocalVoiceInteractionStarted(IBinder token,                IVoiceInteractor voiceInteractor) throws RemoteException {
 . handleTrustStorageUpdate            public void handleTrustStorageUpdate() {
 . scheduleTransaction            public void scheduleTransaction(ClientTransaction transaction) throws RemoteException {
 . requestDirectActions            public void requestDirectActions(@NonNull IBinder activityToken,                @NonNull IVoiceInteractor interactor, @Nullable RemoteCallback cancellationCallback,                @NonNull RemoteCallback callback) {
 . performDirectAction            public void performDirectAction(@NonNull IBinder activityToken, @NonNull String actionId,                @Nullable Bundle arguments, @Nullable RemoteCallback cancellationCallback,                @NonNull RemoteCallback resultCallback) {
 . createSafeCancellationTransport        private @NonNull SafeCancellationTransport createSafeCancellationTransport(            @NonNull CancellationSignal cancellationSignal) {
 . removeSafeCancellationTransport        private @NonNull CancellationSignal removeSafeCancellationTransport(            @NonNull SafeCancellationTransport transport) {
 .         private static final class SafeCancellationTransport extends ICancellationSignal.Stub {
 . cancel            public void cancel() {
 .         class H extends Handler {
 . codeToString            String codeToString(int code) {
 . handleMessage            public void handleMessage(Message msg) {
 .         private class Idler implements MessageQueue.IdleHandler {
 . queueIdle            public final boolean queueIdle() {
 .         final class GcIdler implements MessageQueue.IdleHandler {
 . queueIdle            public final boolean queueIdle() {
 .         final class PurgeIdler implements MessageQueue.IdleHandler {
 . queueIdle            public boolean queueIdle() {
 . currentActivityThread        public static ActivityThread currentActivityThread() {
 . isSystem        public static boolean isSystem() {
 . currentOpPackageName        public static String currentOpPackageName() {
 . currentPackageName        public static String currentPackageName() {
 . currentProcessName        public static String currentProcessName() {
 . currentApplication        public static Application currentApplication() {
 . getPackageManager        public static IPackageManager getPackageManager() {
 . applyConfigCompatMainThread        Configuration applyConfigCompatMainThread(int displayDensity, Configuration config,            CompatibilityInfo compat) {
 . getTopLevelResources        Resources getTopLevelResources(String resDir, String[] splitResDirs, String[] overlayDirs,            String[] libDirs, int displayId, LoadedApk pkgInfo) {
 . getHandler        final Handler getHandler() {
 . getPackageInfo        public final LoadedApk getPackageInfo(String packageName, CompatibilityInfo compatInfo,            int flags) {
 . getPackageInfo        public final LoadedApk getPackageInfo(String packageName, CompatibilityInfo compatInfo,            int flags, int userId) {
 . getPackageInfo        public final LoadedApk getPackageInfo(ApplicationInfo ai, CompatibilityInfo compatInfo,            int flags) {
 . getPackageInfoNoCheck        public final LoadedApk getPackageInfoNoCheck(ApplicationInfo ai,            CompatibilityInfo compatInfo) {
 . peekPackageInfo        public final LoadedApk peekPackageInfo(String packageName, boolean includeCode) {
 . getPackageInfo        private LoadedApk getPackageInfo(ApplicationInfo aInfo, CompatibilityInfo compatInfo,            ClassLoader baseLoader, boolean securityViolation, boolean includeCode,            boolean registerPackage) {
 . isLoadedApkResourceDirsUpToDate        private static boolean isLoadedApkResourceDirsUpToDate(LoadedApk loadedApk,            ApplicationInfo appInfo) {
 . getApplicationThread        public ApplicationThread getApplicationThread()
 . getInstrumentation        public Instrumentation getInstrumentation()
 . isProfiling        public boolean isProfiling() {
 . getProfileFilePath        public String getProfileFilePath() {
 . getLooper        public Looper getLooper() {
 . getExecutor        public Executor getExecutor() {
 . getApplication        public Application getApplication() {
 . getProcessName        public String getProcessName() {
 . getSystemContext        public ContextImpl getSystemContext() {
 . getSystemUiContext        public ContextImpl getSystemUiContext() {
 . createSystemUiContext        public ContextImpl createSystemUiContext(int displayId) {
 . installSystemApplicationInfo        public void installSystemApplicationInfo(ApplicationInfo info, ClassLoader classLoader) {
 . scheduleGcIdler        void scheduleGcIdler() {
 . unscheduleGcIdler        void unscheduleGcIdler() {
 . schedulePurgeIdler        void schedulePurgeIdler() {
 . unschedulePurgeIdler        void unschedulePurgeIdler() {
 . doGcIfNeeded        void doGcIfNeeded() {
 . doGcIfNeeded        void doGcIfNeeded(String reason) {
 .         private static final String HEAP_FULL_COLUMN
 .         private static final String HEAP_COLUMN
 . printRow        static void printRow(PrintWriter pw, String format, Object...objs) {
 . dumpMemInfoTable        public static void dumpMemInfoTable(PrintWriter pw, Debug.MemoryInfo memInfo, boolean checkin,            boolean dumpFullInfo, boolean dumpDalvik, boolean dumpSummaryOnly,            int pid, String processName,            long nativeMax, long nativeAllocated, long nativeFree,            long dalvikMax, long dalvikAllocated, long dalvikFree) {
 . dumpMemoryInfo        private static void dumpMemoryInfo(ProtoOutputStream proto, long fieldId, String name,            int pss, int cleanPss, int sharedDirty, int privateDirty,            int sharedClean, int privateClean,            boolean hasSwappedOutPss, int dirtySwap, int dirtySwapPss) {
 . dumpMemInfoTable        public static void dumpMemInfoTable(ProtoOutputStream proto, Debug.MemoryInfo memInfo,            boolean dumpDalvik, boolean dumpSummaryOnly,            long nativeMax, long nativeAllocated, long nativeFree,            long dalvikMax, long dalvikAllocated, long dalvikFree) {
 . registerOnActivityPausedListener        public void registerOnActivityPausedListener(Activity activity,            OnActivityPausedListener listener) {
 . unregisterOnActivityPausedListener        public void unregisterOnActivityPausedListener(Activity activity,            OnActivityPausedListener listener) {
 . resolveActivityInfo        public final ActivityInfo resolveActivityInfo(Intent intent) {
 . startActivityNow        public final Activity startActivityNow(Activity parent, String id,        Intent intent, ActivityInfo activityInfo, IBinder token, Bundle state,        Activity.NonConfigurationInstances lastNonConfigurationInstances, IBinder assistToken) {
 . getActivity        public final Activity getActivity(IBinder token) {
 . getActivityClient        public ActivityClientRecord getActivityClient(IBinder token) {
 . updatePendingConfiguration        public void updatePendingConfiguration(Configuration config) {
 . updateProcessState        public void updateProcessState(int processState, boolean fromIpc) {
 . updateVmProcessState        private void updateVmProcessState(int processState) {
 . applyPendingProcessState        private void applyPendingProcessState() {
 . countLaunchingActivities        public void countLaunchingActivities(int num) {
 . sendActivityResult        public final void sendActivityResult(            IBinder token, String id, int requestCode,            int resultCode, Intent data) {
 . sendMessage        void sendMessage(int what, Object obj) {
 . sendMessage        private void sendMessage(int what, Object obj, int arg1) {
 . sendMessage        private void sendMessage(int what, Object obj, int arg1, int arg2) {
 . sendMessage        private void sendMessage(int what, Object obj, int arg1, int arg2, boolean async) {
 . sendMessage        private void sendMessage(int what, Object obj, int arg1, int arg2, int seq) {
 . scheduleContextCleanup        final void scheduleContextCleanup(ContextImpl context, String who,            String what) {
 . performLaunchActivity        private Activity performLaunchActivity(ActivityClientRecord r, Intent customIntent) {
 . handleStartActivity        public void handleStartActivity(ActivityClientRecord r,            PendingTransactionActions pendingActions) {
 . checkAndBlockForNetworkAccess        private void checkAndBlockForNetworkAccess() {
 . createBaseContextForActivity        private ContextImpl createBaseContextForActivity(ActivityClientRecord r) {
 .                 for (int id : dm.getDisplayIds()) {
 . handleLaunchActivity        public Activity handleLaunchActivity(ActivityClientRecord r,            PendingTransactionActions pendingActions, Intent customIntent) {
 . reportSizeConfigurations        private void reportSizeConfigurations(ActivityClientRecord r) {
 . deliverNewIntents        private void deliverNewIntents(ActivityClientRecord r, List<ReferrerIntent> intents) {
 . handleNewIntent        public void handleNewIntent(IBinder token, List<ReferrerIntent> intents) {
 . handleRequestAssistContextExtras        public void handleRequestAssistContextExtras(RequestAssistContextExtras cmd) {
 . handleRequestDirectActions        private void handleRequestDirectActions(@NonNull IBinder activityToken,            @NonNull IVoiceInteractor interactor, @NonNull CancellationSignal cancellationSignal,            @NonNull RemoteCallback callback) {
 . handlePerformDirectAction        private void handlePerformDirectAction(@NonNull IBinder activityToken,            @NonNull String actionId, @Nullable Bundle arguments,            @NonNull CancellationSignal cancellationSignal,            @NonNull RemoteCallback resultCallback) {
 . handleTranslucentConversionComplete        public void handleTranslucentConversionComplete(IBinder token, boolean drawComplete) {
 . onNewActivityOptions        public void onNewActivityOptions(IBinder token, ActivityOptions options) {
 . handleInstallProvider        public void handleInstallProvider(ProviderInfo info) {
 . handleEnterAnimationComplete        private void handleEnterAnimationComplete(IBinder token) {
 . handleStartBinderTracking        private void handleStartBinderTracking() {
 . handleStopBinderTrackingAndDump        private void handleStopBinderTrackingAndDump(ParcelFileDescriptor fd) {
 . handleMultiWindowModeChanged        public void handleMultiWindowModeChanged(IBinder token, boolean isInMultiWindowMode,            Configuration overrideConfig) {
 . handlePictureInPictureModeChanged        public void handlePictureInPictureModeChanged(IBinder token, boolean isInPipMode,            Configuration overrideConfig) {
 . handleLocalVoiceInteractionStarted        private void handleLocalVoiceInteractionStarted(IBinder token, IVoiceInteractor interactor) {
 . attemptAttachAgent        private static boolean attemptAttachAgent(String agent, ClassLoader classLoader) {
 . handleAttachAgent        static void handleAttachAgent(String agent, LoadedApk loadedApk) {
 . handleAttachStartupAgents        static void handleAttachStartupAgents(String dataDir) {
 . getIntentBeingBroadcast        public static Intent getIntentBeingBroadcast() {
 . handleReceiver        private void handleReceiver(ReceiverData data) {
 . handleCreateBackupAgent        private void handleCreateBackupAgent(CreateBackupAgentData data) {
 . handleDestroyBackupAgent        private void handleDestroyBackupAgent(CreateBackupAgentData data) {
 . getBackupAgentsForUser        private ArrayMap<String, BackupAgent> getBackupAgentsForUser(int userId) {
 . handleCreateService        private void handleCreateService(CreateServiceData data) {
 . handleBindService        private void handleBindService(BindServiceData data) {
 . handleUnbindService        private void handleUnbindService(BindServiceData data) {
 . handleDumpService        private void handleDumpService(DumpComponentInfo info) {
 . handleDumpActivity        private void handleDumpActivity(DumpComponentInfo info) {
 . handleDumpProvider        private void handleDumpProvider(DumpComponentInfo info) {
 . handleServiceArgs        private void handleServiceArgs(ServiceArgsData data) {
 . handleStopService        private void handleStopService(IBinder token) {
 . performResumeActivity        public ActivityClientRecord performResumeActivity(IBinder token, boolean finalStateRequest,            String reason) {
 . cleanUpPendingRemoveWindows        static final void cleanUpPendingRemoveWindows(ActivityClientRecord r, boolean force) {
 . handleResumeActivity        public void handleResumeActivity(IBinder token, boolean finalStateRequest, boolean isForward,            String reason) {
 . handleTopResumedActivityChanged        public void handleTopResumedActivityChanged(IBinder token, boolean onTop, String reason) {
 . reportTopResumedActivityChanged        private void reportTopResumedActivityChanged(ActivityClientRecord r, boolean onTop,            String reason) {
 . handlePauseActivity        public void handlePauseActivity(IBinder token, boolean finished, boolean userLeaving,            int configChanges, PendingTransactionActions pendingActions, String reason) {
 . performUserLeavingActivity        final void performUserLeavingActivity(ActivityClientRecord r) {
 . performPauseActivity        final Bundle performPauseActivity(IBinder token, boolean finished, String reason,            PendingTransactionActions pendingActions) {
 . performPauseActivity        private Bundle performPauseActivity(ActivityClientRecord r, boolean finished, String reason,            PendingTransactionActions pendingActions) {
 . performPauseActivityIfNeeded        private void performPauseActivityIfNeeded(ActivityClientRecord r, String reason) {
 . performStopActivity        final void performStopActivity(IBinder token, boolean saveState, String reason) {
 .         private static final class ProviderRefCount {
 . ProviderRefCount            ProviderRefCount(ContentProviderHolder inHolder,                ProviderClientRecord inClient, int sCount, int uCount) {
 . performStopActivityInner        private void performStopActivityInner(ActivityClientRecord r, StopInfo info, boolean keepShown,            boolean saveState, boolean finalStateRequest, String reason) {
 . callActivityOnStop        private void callActivityOnStop(ActivityClientRecord r, boolean saveState, String reason) {
 . updateVisibility        private void updateVisibility(ActivityClientRecord r, boolean show) {
 . handleStopActivity        public void handleStopActivity(IBinder token, boolean show, int configChanges,            PendingTransactionActions pendingActions, boolean finalStateRequest, String reason) {
 . reportStop        public void reportStop(PendingTransactionActions pendingActions) {
 . performRestartActivity        public void performRestartActivity(IBinder token, boolean start) {
 . handleWindowVisibility        public void handleWindowVisibility(IBinder token, boolean show) {
 . handleSleeping        private void handleSleeping(IBinder token, boolean sleeping) {
 . handleSetCoreSettings        private void handleSetCoreSettings(Bundle coreSettings) {
 . onCoreSettingsChange        private void onCoreSettingsChange() {
 . updateDebugViewAttributeState        private boolean updateDebugViewAttributeState() {
 . relaunchAllActivities        private void relaunchAllActivities(boolean preserveWindows) {
 . handleUpdatePackageCompatibilityInfo        private void handleUpdatePackageCompatibilityInfo(UpdateCompatibilityData data) {
 . deliverResults        private void deliverResults(ActivityClientRecord r, List<ResultInfo> results, String reason) {
 . handleSendResult        public void handleSendResult(IBinder token, List<ResultInfo> results, String reason) {
 . performDestroyActivity        ActivityClientRecord performDestroyActivity(IBinder token, boolean finishing,            int configChanges, boolean getNonConfigInstance, String reason) {
 . safeToComponentShortString        private static String safeToComponentShortString(Intent intent) {
 . getActivitiesToBeDestroyed        public Map<IBinder, ClientTransactionItem> getActivitiesToBeDestroyed() {
 . handleDestroyActivity        public void handleDestroyActivity(IBinder token, boolean finishing, int configChanges,            boolean getNonConfigInstance, String reason) {
 . prepareRelaunchActivity        public ActivityClientRecord prepareRelaunchActivity(IBinder token,            List<ResultInfo> pendingResults, List<ReferrerIntent> pendingNewIntents,            int configChanges, MergedConfiguration config, boolean preserveWindow) {
 . handleRelaunchActivity        public void handleRelaunchActivity(ActivityClientRecord tmp,            PendingTransactionActions pendingActions) {
 . scheduleRelaunchActivity        void scheduleRelaunchActivity(IBinder token) {
 . handleRelaunchActivityLocally        private void handleRelaunchActivityLocally(IBinder token) {
 . handleRelaunchActivityInner        private void handleRelaunchActivityInner(ActivityClientRecord r, int configChanges,            List<ResultInfo> pendingResults, List<ReferrerIntent> pendingIntents,            PendingTransactionActions pendingActions, boolean startsNotResumed,            Configuration overrideConfig, String reason) {
 . reportRelaunch        public void reportRelaunch(IBinder token, PendingTransactionActions pendingActions) {
 . callActivityOnSaveInstanceState        private void callActivityOnSaveInstanceState(ActivityClientRecord r) {
 . collectComponentCallbacks        ArrayList<ComponentCallbacks2> collectComponentCallbacks(            boolean allActivities, Configuration newConfig) {
 . performConfigurationChangedForActivity        private void performConfigurationChangedForActivity(ActivityClientRecord r,            Configuration newBaseConfig) {
 . performConfigurationChangedForActivity        private Configuration performConfigurationChangedForActivity(ActivityClientRecord r,            Configuration newBaseConfig, int displayId, boolean movedToDifferentDisplay) {
 . createNewConfigAndUpdateIfNotNull        private static Configuration createNewConfigAndUpdateIfNotNull(@NonNull Configuration base,            @Nullable Configuration override) {
 . performConfigurationChanged        private void performConfigurationChanged(ComponentCallbacks2 cb, Configuration newConfig) {
 . performActivityConfigurationChanged        private Configuration performActivityConfigurationChanged(Activity activity,            Configuration newConfig, Configuration amOverrideConfig, int displayId,            boolean movedToDifferentDisplay) {
 . applyConfigurationToResources        public final void applyConfigurationToResources(Configuration config) {
 . applyCompatConfiguration        final Configuration applyCompatConfiguration(int displayDensity) {
 . handleConfigurationChanged        public void handleConfigurationChanged(Configuration config) {
 . handleConfigurationChanged        private void handleConfigurationChanged(Configuration config, CompatibilityInfo compat) {
 . handleSystemApplicationInfoChanged        public void handleSystemApplicationInfoChanged(@NonNull ApplicationInfo ai) {
 . handleApplicationInfoChanged        public void handleApplicationInfoChanged(@NonNull final ApplicationInfo ai) {
 . freeTextLayoutCachesIfNeeded        static void freeTextLayoutCachesIfNeeded(int configDiff) {
 . updatePendingActivityConfiguration        public void updatePendingActivityConfiguration(IBinder activityToken,            Configuration overrideConfig) {
 . handleActivityConfigurationChanged        public void handleActivityConfigurationChanged(IBinder activityToken,            Configuration overrideConfig, int displayId) {
 . handleProfilerControl        final void handleProfilerControl(boolean start, ProfilerInfo profilerInfo, int profileType) {
 . stopProfiling        public void stopProfiling() {
 . handleDumpHeap        static void handleDumpHeap(DumpHeapData dhd) {
 . handleDispatchPackageBroadcast        final void handleDispatchPackageBroadcast(int cmd, String[] packages) {
 . handleLowMemory        final void handleLowMemory() {
 . handleTrimMemory        private void handleTrimMemory(int level) {
 . setupGraphicsSupport        private void setupGraphicsSupport(Context context) {
 . updateDefaultDensity        private void updateDefaultDensity() {
 . getInstrumentationLibrary        private String getInstrumentationLibrary(ApplicationInfo appInfo, InstrumentationInfo insInfo) {
 . updateLocaleListFromAppContext        private void updateLocaleListFromAppContext(Context context, LocaleList newLocaleList) {
 . handleBindApplication        private void handleBindApplication(AppBindData data) {
 . installContentProviders        private void installContentProviders(            Context context, List<ProviderInfo> providers) {
 . acquireProvider        public final IContentProvider acquireProvider(            Context c, String auth, int userId, boolean stable) {
 . getGetProviderLock        private Object getGetProviderLock(String auth, int userId) {
 . incProviderRefLocked        private final void incProviderRefLocked(ProviderRefCount prc, boolean stable) {
 . acquireExistingProvider        public final IContentProvider acquireExistingProvider(            Context c, String auth, int userId, boolean stable) {
 . releaseProvider        public final boolean releaseProvider(IContentProvider provider, boolean stable) {
 . completeRemoveProvider        final void completeRemoveProvider(ProviderRefCount prc) {
 . handleUnstableProviderDied        final void handleUnstableProviderDied(IBinder provider, boolean fromClient) {
 . handleUnstableProviderDiedLocked        final void handleUnstableProviderDiedLocked(IBinder provider, boolean fromClient) {
 . appNotRespondingViaProvider        final void appNotRespondingViaProvider(IBinder provider) {
 . installProviderAuthoritiesLocked        private ProviderClientRecord installProviderAuthoritiesLocked(IContentProvider provider,            ContentProvider localProvider, ContentProviderHolder holder) {
 . installProvider        private ContentProviderHolder installProvider(Context context,            ContentProviderHolder holder, ProviderInfo info,            boolean noisy, boolean noReleaseNeeded, boolean stable) {
 . Slog.e                        Slog.e(TAG, "Failed to instantiate class " +
 . handleRunIsolatedEntryPoint        private void handleRunIsolatedEntryPoint(String entryPoint, String[] entryPointArgs) {
 . attach        private void attach(boolean system, long startSeq) {
 . systemMain        public static ActivityThread systemMain() {
 . updateHttpProxy        public static void updateHttpProxy(@NonNull Context context) {
 . installSystemProviders        public final void installSystemProviders(List<ProviderInfo> providers) {
 . getIntCoreSetting        public int getIntCoreSetting(String key, int defaultValue) {
 .         private static class AndroidOs extends ForwardingOs {
 . install            public static void install() {
 . AndroidOs            private AndroidOs(Os os) {
 . openDeprecatedDataPath            private FileDescriptor openDeprecatedDataPath(String path, int mode) throws ErrnoException {
 . deleteDeprecatedDataPath            private void deleteDeprecatedDataPath(String path) throws ErrnoException {
 . access            public boolean access(String path, int mode) throws ErrnoException {
 . open            public FileDescriptor open(String path, int flags, int mode) throws ErrnoException {
 . stat            public StructStat stat(String path) throws ErrnoException {
 . unlink            public void unlink(String path) throws ErrnoException {
 . remove            public void remove(String path) throws ErrnoException {
 . rename            public void rename(String oldPath, String newPath) throws ErrnoException {
 . main        public static void main(String[] args) {
 . purgePendingResources        private void purgePendingResources() {
