define(["bubble","jquery"], function(bubble, jquery) {

    function bubbleSource(x, y, height, name, birthrate, lifeExpectancy, context, bubbleColour, alpha) {
        this.x = x;
        this.y = y;
        this.height = height;
        this.name = name;
        this.birthrate = birthrate;
        this.lifeExpectancy = lifeExpectancy;
        this.normalizedBirthrate = 0;
        this.normalizedLifeExpectancy = 0;
        this.context = context;
        this.bubbleColour = bubbleColour;
        this.bubbleAlpha = alpha;
        this.milliSecSinceLastBubble = 0;
        this.lastBubble = 0;
        this.noramlized = false;
        this.bubbles = [];
        this.deadBubbles = [];
        this.active = false;
    }

    bubbleSource.prototype = {
        update: function () {
            if(this.noramlized && this.active) {
                this.milliSecSinceLastBubble = Date.now() - this.lastBubble;

                if(this.milliSecSinceLastBubble >= (this.normalizedBirthrate)*10000){
                    this.lastBubble = Date.now();
                    var b = new bubble(this.x, this.y, this.height, this.normalizedLifeExpectancy, this.context, this.bubbleColour, this.bubbleAlpha);
                    this.bubbles.push(b);
                }

                for(i = 0; i < this.bubbles.length; i++){
                    this.bubbles[i].update();
                    if(this.bubbles[i].isDead()){
                        this.bubbles.splice(i,1);
                        i--;
                    }
                }
            }
        },
        draw: function () {
            if(this.active) {
                this.context.globalAlpha=1;
                this.context.fillStyle="#FFF";
                this.context.fillText("Country: " +this.name,this.x-85,this.y+15);
                this.context.fillText("Birthrate: " +this.birthrate + "(" + this.normalizedBirthrate +")",this.x-85,this.y+30);
                this.context.fillText("Life expectancy: " +this.lifeExpectancy + "(" + this.normalizedLifeExpectancy + ")",this.x-85,this.y+45);
                for(i = 0; i < this.bubbles.length; i++){
                    this.bubbles[i].draw();
                }
            }
        }
    };

    return bubbleSource;
});