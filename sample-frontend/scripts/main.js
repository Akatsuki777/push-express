document.addEventListener('DOMContentLoaded', async() =>{

    const isSubscribed = await getSubscriptionStatus();
    const subscribeButton = document.querySelector('.pe-subscribe-btn');
    
    //Display subscribe button only to unsubscribed clients with notifications available in window
    if (isSubscribed || !("Notification" in window)){
        subscribeButton.setAttribute("style","display: none;");
    }

    const jsonData = await getJSONData();

    if (jsonData == {}){
        return;
    }

    const scoreArea = document.querySelector('.pe-info-card-score');
    const programArea = document.querySelector('.pe-info-card-draw-scheme');
    const dateArea = document.querySelector('.pe-info-card-draw-date');

    scoreArea.textContent = jsonData['score'];
    programArea.textContent = jsonData['program'];
    dateArea.textContent = jsonData['date'];
})

async function getSubscriptionStatus(){

    const subscribed = 'Notification' in window &&
    'serviceWorker' in navigator && 'PushManager' in window;

    if(!subscribed){
        return false;
    }

    const permission = Notification.permission;
    const registration = await navigator.serviceWorker.getRegistration();
    const notificationSubscription = await registration? registration.pushManager.getSubscription():null;

    if (permission === 'granted' && notificationSubscription){
        return true;
    }

    return false;
}

async function getJSONData(){
    
    const response = await fetch('/get_data');

    if (response.status != 200){
        throw new Error("Invalid response! No JSON data received!");
    }

    const data = await response.json();

    if (data['score']){
        return data;
    } 

    return {};
}

async function subscribe(){

    const permission = await Notification.requestPermission();

    if (permission !== 'granted'){
        alert("Permission Denied!");
        return;
    }

    const registration = await navigator.serviceWorker.register('/sw.js');

    const keyRes = await fetch("/vapid_key");
    const { publicKey } = await keyRes.json();

    const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(publicKey),
    });

    await fetch("/subscribe",{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(subscription),
    });
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, "+")
    .replace(/_/g, "/");

  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}