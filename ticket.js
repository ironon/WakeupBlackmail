
const fs = require("fs")
const {createCanvas, loadImage} = require('canvas')

const { sendInfoToServer } = require('./sendToServer.js')





const TOTAL_SIGS = 10 //The number of signatures in the sigs folder
let SIG_NUMBER
try {
    SIG_NUMBER = (JSON.parse(fs.readFileSync("sigs.json")).number) % TOTAL_SIGS
} catch(e) {
    SIG_NUMBER = 0
}



function getDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = mm + '/' + dd + '/' + yyyy;
    return today
}
function getLines(ctx, text, maxWidth) {
    var words = text.split(" ");
    var lines = [];
    var currentLine = words[0];

    for (var i = 1; i < words.length; i++) {
        var word = words[i];
        var width = ctx.measureText(currentLine + " " + word).width;
        if (width < maxWidth) {
            currentLine += " " + word;
        } else {
            lines.push(currentLine);
            currentLine = word;
        }
    }
    lines.push(currentLine);
    return lines;
}
class Lines {
    static subtitles = ["with honey, anything's free :D", "DONT CLICK CLAIM PLZ", "tell me to write more qutoes for this", "make sure to use this ticket for evil terrible things", "i will inflate the david ticket economy", "no screenshotting my NFTS!!!!", "this is classified as an NFT", "trademarked and copywrited. now i own YOU", "this quote is definetly not randomly generated.", "help", "buy one get none free!!!", "by claiming this you agree to not playing skyblock for the next 24 hours", "by claiming this you agree david is infinitely cooler than you", "im sorry but im confiscating your rights"]
    static descriptions = this.subtitles
    static pickSubtitle() {
        return this.subtitles[Math.floor(Math.random() * this.subtitles.length)]
    }
    static pickDescription() {
        return this.descriptions[Math.floor(Math.random() * this.subtitles.length)]
    }
}

class Ticket {
    constructor(color, subtitle, desc) {
        this.color = color || 'red'
        this.subtitle = subtitle || Lines.pickSubtitle()
        this.desc = desc ||Lines.pickDescription()
        this.image = this.createImage()
        fs.writeFile('sigs.json', JSON.stringify({number: SIG_NUMBER + 1}), (err) => {
            //pass
        })

    }
    toJSON() {
        //This must return an object
        
        return {date: getDate(), subtitle: this.subtitle, desc: this.desc, image:this.imageURL}
        //UNFINISHED
    }
    createImage() {
        const width = 1600
        const height = 1200

        const canvas = createCanvas(width, height)
        const ctx = canvas.getContext("2d")
        
        //background and border
        ctx.fillStyle = this.color
        ctx.fillRect(0, 0, width, height)
        ctx.fillStyle = 'white'
        ctx.fillRect(width * 0.03, height * 0.03, width * 0.94, height * 0.94)

        //title
        ctx.font = "120px Comic Sans MS"
        ctx.fillStyle = "black"
        ctx.textAlign = 'center';
        ctx.fillText("DAVID TICKET", width * 0.5, height * 0.3)
        
        //date
        ctx.font = "30px Comic Sans MS"
        ctx.fillStyle = "gray"
        ctx.textAlign = 'center';
        ctx.fillText(getDate(), width * 0.5, height * 0.18)

        //subtitle
        ctx.font = "50px Comic Sans MS"
        ctx.fillStyle = "gray"
        ctx.textAlign = 'center';
        let i = 0
        getLines(ctx, this.subtitle, width * 0.9).forEach((line) => {
            ctx.fillText(line, width * 0.5, height * (0.4 + (i * 0.06)))
            i++
        })

         //desc
         ctx.font = "35px Comic Sans MS"
         ctx.fillStyle = "black"
         ctx.textAlign = 'center';
         i = 0
         getLines(ctx, this.desc, width * 0.9).forEach((line) => {
             ctx.fillText(line, width * 0.5, height * (0.55 + (i * 0.06)))
             i++
         })

         //signature
         loadImage('./sigs/sig' + SIG_NUMBER + '.png').then(imageObj => {
            
            ctx.drawImage(imageObj, width * 0.2, height * 0.8, 1000, 1000 * imageObj.height / imageObj.width)
        }).then(() => {
            const buffer = canvas.toBuffer('image/png')
            fs.writeFileSync('./output/latest.png', buffer)
            this.imageURL = canvas.toDataURL('image/png')
            console.log("Saved Ticket!")
        }).then(() => {
            addTicket(this)
        })
        



        
    }
    
}

function addTicket(ticketClass) {
    console.log("Sending ticket to server...")
    ticketClass = JSON.parse(JSON.stringify(ticketClass))
    sendInfoToServer(ticketClass)
    
    
    
}
const args = process.argv
new Ticket(args[4], args[2], args[3])
