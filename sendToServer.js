



const { ref, set} = require("firebase/database")

var admin = require("firebase-admin");

var serviceAccount = require("./secret.json");
let app = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount["firebase"]),
    databaseURL: "https://davidticketsimulator-default-rtdb.firebaseio.com"
  });

const db = admin.database()
const reference = ref(db, "tickets/")


let ticketData
const sendInfoToServer = (data) => {
    setTimeout(() => {
      ticketData = data
      set(reference, ticketData)
    },1500)
    setTimeout(() => {
      process.exit(0)
    }, 3000)
    
}






module.exports = { sendInfoToServer }