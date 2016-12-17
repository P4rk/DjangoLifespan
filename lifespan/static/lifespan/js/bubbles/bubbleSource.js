define(["bubble","jquery"], function(bubble, jquery) {

    /**
     * Bubble source definition. Creates bubbles at a rate relatively the birthrate and 
     * that will grow relatively to the lifeExpectancy.
     * @param x the x position of the bubble source
     * @param y the y position of the bubble source
     * @param height the of the bubble source (same as y)
     * @param name the name of this bubble source, often the name of the country
     * @param birthrate the birth rate of the country
     * @param lifeExpectancy the life expectancy of the country.
     * @param context the 2d context of the canvas
     * @param bubbleColour the color the bubbles should be created in
     * @param alpha the alpha level the bubbles should start at
     */
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
        /**
         * Update function that decides if it needs to create a new bubble or 
         * remove any current bubbles form the screen. 
         * Updates all bubbles belonging to this source.
         */
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
        /**
         * Draw function that displays the birth rate and life expectancy for the 
         * bubble source. Also calls draw on all of the current bubbles.
         */
        draw: function () {
            if(this.active) {
                this.context.globalAlpha=0.1;
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