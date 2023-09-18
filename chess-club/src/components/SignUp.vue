<template>
    <div class="container">
        
        <div class="left-div">
            <p class="quote">{{ currentQuote }}</p>
            <!-- Content for the left div -->

        </div>
        
        <div class="right-div">
            <div class="circular-div">
    <!-- Content for the circular div (e.g., icon, text) -->
    <div class = "sign-up">
                <div class="top-div">
                    <img class="logo" src="../assets/logo1.png" />
                    <h1>Sign Up</h1>
                    
                </div>

            <div class="register">
                <input type="text" placeholder="Enter name" />
                <input type="text" placeholder="Enter Email" />
                <input type="password" placeholder="Enter Password" />
                <button>Sign Up</button>
            </div>
        </div>

  </div>
            
</div>
</div>
</template>

<script>
        export default{
            name:'SignUp',
            data() {
    return {
      quotes: [
        "Chess is the gymnasium of the mind. - Blaise Pascal",
        "In chess, as in life, a move is not necessarily good just because it's flashy. - Bill Gates",
        "Chess is a war over the board. The object is to crush the opponent’s mind. - Bobby Fischer",
        "Chess is mental torture. - Garry Kasparov",
        "The biggest challenge in chess is not defeating your opponent, but defeating yourself. - unknown",
        "Chess is ruthless: you've got to be prepared to kill people. - Nigel Short",
        "A good player is always lucky. - Capablanca",
        "In chess, just as in life, today's bliss may be tomorrow's poison. - Assaic",
        "Chess is a cold bath for the mind. - Sir John Simon",
        "No price is too great for the scalp of the enemy king. - Koblentz",
      ],
      currentIndex: 0,
    };
  },
  computed: {
    currentQuote() {
      return this.quotes[this.currentIndex];
    },
  },
  created() {
    // Start the timer to rotate quotes
    setInterval(this.rotateQuote, 7000); // 15 seconds interval
  },
  methods: {
    rotateQuote() {
      // Increment the currentIndex and loop back to the beginning if needed
      this.currentIndex = (this.currentIndex + 1) % this.quotes.length;
    },
  },
};
        
</script>
<style>
.logo{
    widows: 100px;
    height: 100px;
}
.register input {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 20px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid skyblue;

}
.register button{
    width: 270px;
    height: 40px;
    border: 1px solid #DC2543 ;
    background: #DC2543 ;
    color: aliceblue;
    cursor: pointer;
}
.register{
    padding: 20px;
}
html, body {
  height: 100%; /* Ensure the body and HTML element take up the full height of the viewport */
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.container {
  display: flex;
  width: 100%;
  height: 100vh; /* Use 100vh (viewport height) to make the container take up the full height of the viewport */
}

.left-div,
.right-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%; /* Adjust the width as needed */
  margin: 0 auto;
  background-color: #f0f0f0; /* Background color for the right-div */
  padding: 20px;
  box-sizing: border-box; /* Ensure padding and border are included in the width calculation */
}

.left-div {
  background-color:#1E94A0  ; /* Background color for the left div */
  background-image: url('../assets/bg-for-left-div.png'); /* Replace 'path/to/' with the actual path to your image */
  background-size: cover; /* Adjust the background size as needed */
  background-repeat: no-repeat;
  background-position: center center;
}

.right-div {
  background-color:#004E6D ; /* Background color for the right div */
  
}

.top-div {
  background-color: #DC2543 ; /* Background color for the top-div */
  padding: 20px;
  border-radius: 6%;
  text-align: center;
}
.sign-up {
  background-color: #faf7f5; /* Background color for the sign-up div */
  border-radius: 6%;
  text-align: center;
  width: auto; /* Allow the div to take up only the space required by its content */
}
.circular-div {
  width: 540px;
  height: 580px;
  background-color: #FEC0C1 ; /* Background color for the circular div */
  border-radius: 50%; /* Create a circular shape */
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff; /* Text color inside the circular div */
  font-size: 24px; /* Font size for the content inside the circular div */
  font-weight: bold; /* Bold text */
  text-transform: uppercase; /* Uppercase text */
}
.quote {
  font-size: 35px; /* Adjust the font size as needed */
  color: #251f1f; /* Set the text color to white */
  font-weight: bold; /* Make the text bold */
}
</style>