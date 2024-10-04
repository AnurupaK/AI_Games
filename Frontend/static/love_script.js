// // Function to set the progress dynamically
// function setProgress(percentage) {
//     const circle = document.querySelector('.circle');
//     const text = document.querySelector('.percentage');
    
//     // Calculate stroke-dasharray based on the percentage
//     const dashArray = `${percentage}, 100`;

//     // Update the circle's stroke-dasharray and percentage text
//     circle.setAttribute('stroke-dasharray', dashArray);
//     text.textContent = `${percentage}%`;
// }

// // Assuming you'll get the percentage from Flask
// // Example: If Flask sends a value through an API or directly to the page
// let lovePercentage = 20; // Replace this with the actual percentage from Flask

// // Set the progress when the page loads
// setProgress(lovePercentage);


document.addEventListener('DOMContentLoaded', async function(){
    let you = document.querySelector('.first_name')
    let he = document.querySelector('.last_name')
    let calculate = document.querySelector('.calculate_love')
    let text = document.querySelector('.love_text')
    let emoji_box = document.querySelector('.love_emoji')
    let love_restart = document.querySelector('.love_restart')


    if(love_restart){
        love_restart.addEventListener('click',async function(){
            you.value = ""
            he.value = ""
            emoji_box.style.backgroundColor = 'white';
            emoji_box.innerHTML = "🍃"
            setProgress(0)
            text.innerHTML = ""
            percentage = 0
        })
    }
    if (calculate){
        calculate.addEventListener('click',async function(){
            if(you.value && he.value){
                   let {percentage,message,emo} = await SendNamesAI(you.value,he.value)
                   console.log(percentage)
                   console.log(emo)
                   await setProgress(percentage)
                   text.innerHTML =  message
                   emoji_box.innerHTML = emo
                   emoji_box.style.backgroundColor = 'yellow';
                   percentage = 0

                   
            }
            else{
                text.innerHTML = "Add your and partner name"
            }
        })
    }
    
})


async function SendNamesAI(your_name,partner_name) {
    try {
        let response = await fetch('/api/lovePercentage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'your_name':your_name,'partner_name':partner_name})
        });
        let data = await response.json();
        console.log(data);
        return {
            percentage: data.percentage,
            message: data.message,
            emo: data.emoji
        }
    } catch (error) {
        console.error("AI didn't say anything");
    }
}


// Function to set the progress dynamically
async function setProgress(percentage) {
    const circle = document.querySelector('.circle');
    const text = document.querySelector('.percentage');
    
    const dashArray = `${percentage}, 100`;


    circle.setAttribute('stroke-dasharray', dashArray);
    text.textContent = `${percentage}%`;
}

