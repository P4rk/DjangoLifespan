define([], function() {

    /**
     * Bubble definition. 
     * @param x the x position of the bubble source
     * @param y the y position of the bubble source
     * @param height the of the bubble source (same as y)
     * @param normalizedLifeExpectancy the normalized life expectancy of the country.
     * @param context the 2d context of the canvas
     * @param bubbleColour the color the bubble should be created in
     * @param bubbleAlpha the alpha level the bubble should start at
     */
    function bubble(x, y, height, normalizedLifeExpectancy, context, bubbleColour, bubbleAlpha) {
         this.x = x;
         this.y = y;
         this.height = height;
         this.startHeight = y;
         this.normalizedLifeExpectancy = normalizedLifeExpectancy;
         this.scale = 1;
         this.dead = false;
         this.context = context;
         this.colour = bubbleColour;
         this.alpha = bubbleAlpha;
         this.normalisedY = 0;
    }

    bubble.prototype = {
        /**
         * Update function that moves the bubble and decides if it should still exist.
         */
        update: function()
        {
            this.normalisedY = (((this.height-this.y)-0)/(this.height-0));
            this.scale =  (60 * this.normalisedY);
            this.y -= 1;

            if(this.normalizedLifeExpectancy <= this.normalisedY){
                this.dead = true;
            }
        },
        /**
         * Draw function that draws the bubble.
         */
        draw: function (){
            this.context.beginPath();
            this.context.globalAlpha =  1 -this.normalisedY ;
            this.context.fillStyle = this.colour;
            this.context.arc(this.x,this.y,this.scale+1,0,2*Math.PI);
            this.context.fill();
        },
        /**
         * A function returning whether the bubble should still exist.
         */
        isDead: function() {
            return this.dead;
        }
    };
    return bubble;
});