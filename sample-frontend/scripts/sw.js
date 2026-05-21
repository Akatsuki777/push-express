self.addEventListener("push",(event)=>{
    const data = event.data? event.data.json() : {};

    event.waitUntil(
        self.registration.showNotification(data.title || "New Update",{
            body: data.body || "Somethign changed",
            data: data.url || '/'
        })
    );
});

self.addEventListener("notificationclick",(event)=>{
    event.notification.close();

    event.waitUntil(
        clients.openWindow(event.notification.data || "/")
    );
});