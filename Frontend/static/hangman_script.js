let mistake = 1
let blank_count = 0
let guessedLetters = {};
document.addEventListener('DOMContentLoaded', async function () {
    let word, hint, indexWord;

    const start = document.querySelector('.start_button');
    const alphabets = document.querySelectorAll(".key");
    const light = document.querySelector(".light_image");
    const text = document.querySelector(".text_area");
    const blank_area = document.querySelector(".blank_space");
    // const hangman = document.querySelector(".hangman_images")

    if (start) {
        console.log("Start button found");
        

        start.addEventListener('click', async function () {
            document.querySelector('.hangman_images').style.backgroundImage = `url('static/images/hangman1.png')`;
            mistake = 1
            blank_count = 0
            guessedLetters ={}
            text.innerHTML = " ";
            blank_area.innerHTML = "";
            const response = await ai_function();

            word = response.word;
            hint = response.hint;
            indexWord = response.indexWord;

            console.log(word);
            console.log(hint);
            console.log(indexWord);

            let blanks = word.length;
            for (let i = 0; i < blanks; i++) {
                let blanks_box = document.createElement('div');
                blanks_box.className = `hello hello${i}`;
                blank_area.append(blanks_box);
            }
            console.log(blanks);

            if (light) {
                light.addEventListener('click', async function () {
                    text.innerHTML = hint;
                });
            } else {
                light.addEventListener('click', async function () {
                    text.innerHTML = "Sorry! I can't provide you with a hint";
                });
            }
        });
    }

    alphabets.forEach(letter => {
        letter.addEventListener('click', async function () {
            const clickedLetter = letter.innerHTML;
            let { letterUser, message } = await alphabets_send(clickedLetter);
            if(letterUser && message){
                console.log(letterUser)
                console.log(message)
            }
            if (indexWord) {
                let letterFound = false;

                for (const true_letter in indexWord) {
                    if (true_letter === clickedLetter) {

                        letterFound = true;
                        console.log(`Letter ${true_letter} found at indices: ${indexWord[true_letter]}`);


                        indexWord[true_letter].forEach(index => {

                            if (!guessedLetters[true_letter]) {
                                guessedLetters[true_letter] = [];
                            }

                            if (!guessedLetters[true_letter].includes(index)) {
                                blank_count = blank_count + 1;
                                console.log("Blanks Filled",blank_count)
                                let box = document.querySelector(`.hello${index}`);
                                if (box) {
                                    box.innerHTML = true_letter;
                                    guessedLetters[true_letter].push(index);
                                    if(message!=0)
                                    {
                                    text.innerHTML = message
                                    }
                                    else{
                                        text.innerHTML = "Yayyy! You got one! Keep going😉"
                                    }
                                } else {
                                    text.innerHTML = `"Oops! 😅 Looks like the word hasn't been generated yet or you're already a pro and finished! 🎉 Ready for another round? 🔄✨"`;
                                }
                            } else {
                                text.innerHTML = `"Hey! You've already selected '${true_letter}'! Try something else! 😎🚫"`;
                            }
                        });
                    }
                }
                if (blank_count == word.length) {
                    setTimeout(() => {
                       
                            blank_area.innerHTML = "🎉 Woohoo! You nailed it! 🏆 You won! Time to celebrate! 🎊🎉"
                        

                    }, 1000);

                }

                if (!letterFound) {
                    if (message != 0) {
                        text.innerHTML = message
                    }
                    else {
                        text.innerHTML = ` "Uh-oh! 🚫 ${clickedLetter} doesn't seem to be part of the word. Keep going, you're getting closer! 🎯🔍"`;
                    }
                    mistake = mistake + 1
                    if (mistake <= 7) {
                        document.querySelector('.hangman_images').style.backgroundImage = `url('static/images/hangman${mistake}.png')`;
                    }


                    if (mistake == 7) {

                            blank_area.innerHTML = "💔 Oh no! Looks like the word slipped away this time. You lost! But don't worry, there's always another chance! 🔄😅"
                        
                    }



                }
            } else {
                text.innerHTML = "Oops! The word is in the baking. Lets start the game😎";
            }
        });
    });
});

async function ai_function() {
    try {
        let response = await fetch('/api/gemini', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        let data = await response.json();
        console.log(data);
        return {
            word: data.Word,
            hint: data.Hint,
            indexWord: data.Word_Index_Counter
        };
    } catch (error) {
        console.error("No gemini response");
    }
}

async function alphabets_send(letter) {
    try {
        let response = await fetch('/api/guessed_letter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'letter': letter })
        });
        let data = await response.json();
        console.log(data);
        return {
            letterUser: data.letterUser,
            message: data.message
        }
    } catch (error) {
        console.error("No alphabet chosen");
    }
}
