let check_status = false
let totalAttempts = 0
let count = 5
document.addEventListener('DOMContentLoaded', async function () {
    let box = document.querySelector('.riddle_box')
    let commentry = document.querySelector('.commentry')
    let text = document.querySelector('.riddle_text')
    let start = document.querySelector('.riddle_start')
    let check = document.querySelector('.riddle_check')
    let restart = document.querySelector('.riddle_restart')
    const riddleCircle = document.querySelector('.riddle_circle');

 
    if (restart) {
        restart.addEventListener('click', async function () {
            check_status = false;
            totalAttempts = 0;
            count = 5;

            box.innerHTML = " ";
            text.value = " ";
            commentry.innerHTML = " ";
    
            const riddleCircle = document.querySelector('.riddle_circle');
            

            riddleCircle.innerHTML = '';
    

            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '150');
            svg.setAttribute('height', '150');
            svg.setAttribute('viewBox', '0 0 36 36');
            svg.setAttribute('class', 'circular-chart2');
    
            const circleBg = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            circleBg.setAttribute('class', 'circle-bg2');
            circleBg.setAttribute('d', 'M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831');
    
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            circle.setAttribute('class', 'circle2');
            circle.setAttribute('stroke-dasharray', '0, 100');
            circle.setAttribute('d', 'M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831');
    
            const textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            textElement.setAttribute('x', '18');
            textElement.setAttribute('y', '20.35');
            textElement.setAttribute('class', 'lives');
            textElement.textContent = '5';

            svg.appendChild(circleBg);
            svg.appendChild(circle);
            svg.appendChild(textElement);
    
            riddleCircle.appendChild(svg);
        });
    }
    

    if (start) {
        start.addEventListener('click', async function () {
            let { riddle, answer } = await GetRiddleAI()
            check_status = true
            box.innerHTML = riddle
            console.log(answer)
        })
    }

    if (check) {
        console.log("Check found")
        check.addEventListener('click', async function () {
            if (check_status) {
                console.log("Check can be used")


                if (text.value) {
                    console.log("Text",text.value)
                    let { AIcomment, answer_status } = await ReturnAIResponse(text.value)
                    console.log(AIcomment)
                    commentry.innerHTML = AIcomment
                    if (answer_status == 'no') {
                        totalAttempts = totalAttempts + 1
                        console.log("Total Attempts:", totalAttempts)
                        percentage = totalAttempts * 20
                        count = count - 1
                        await setProgressNew(percentage, count)

                        if (totalAttempts >= 5) {
                            commentry.innerHTML = "Not the answer I was looking for. Want to try again? 🤷‍♂️"
                            // box.innerHTML = " "
                            // await setProgress(100, 0)
                            riddleCircle.innerHTML = " "
                            const gifImage = document.createElement('img');
                            gifImage.src = 'static/images/loser.gif';
                            gifImage.alt = 'Description of GIF'; 
                            gifImage.className = 'riddle-gif';
                            riddleCircle.append(gifImage);
                        }

                    } 
                    else {
                        riddleCircle.innerHTML = " "
                        const gifImage = document.createElement('img');
                        gifImage.src = 'static/images/winner.gif';
                        gifImage.alt = 'Description of GIF'; 
                        gifImage.className = 'riddle-gif';
                        riddleCircle.append(gifImage);
                        
                    }

                }
                else {
                    console.log("Text",text.value)
                    commentry.innerHTML = "Write some answer"
                }

            } else {
                console.log("Check can't be used")
                commentry.innerHTML = "Umm, I can't see any riddle for which you are answering!🤔"
            }
        })
    }
})





async function GetRiddleAI() {
    try {
        let response = await fetch('/api/riddleGenerate', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        let data = await response.json();
        console.log(data);
        return {
            riddle: data.riddle,
            answer: data.answer
        }
    } catch (error) {
        console.error("AI didn't riddle anything");
    }
}

async function ReturnAIResponse(answer_to_check) {
    try {
        let response = await fetch('/api/aiComment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'answer_to_check': answer_to_check })
        });
        let data = await response.json();
        console.log(data);
        return {
            AIcomment: data.AIcomment,
            answer_status: data.answer_status
        }
    } catch (error) {
        console.error("AI didn't comment anything");
    }
}


async function setProgressNew(percentage, count) {
    const circle = document.querySelector('.circle2');
    const text = document.querySelector('.lives');

    const dashArray = `${percentage}, 100`;


    circle.setAttribute('stroke-dasharray', dashArray);
    text.textContent = `${count}`;
}

