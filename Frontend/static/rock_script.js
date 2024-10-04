document.addEventListener('DOMContentLoaded', async function () {
    let rock = document.querySelector('.rock')
    let paper = document.querySelector('.paper')
    let scissor = document.querySelector('.scissor')
    let text_rock = document.querySelector('.text_rock')
    let ai_rock = document.querySelector('.ai_rock')
    const rockItem = document.querySelector('.rock_item') 
    const paperItem = document.querySelector('.paper_item')
    const scissorItem = document.querySelector('.scissor_item')
    let restart = document.querySelector('.restart')

    if(restart){
        console.log("Restart found")
        restart.addEventListener('click',async function () {
            rockItem.style.backgroundColor = 'white';
            paperItem.style.backgroundColor = 'white';
            scissorItem.style.backgroundColor = 'white';
            text_rock.innerHTML = " "
            ai_rock.innerHTML = " "
        })
    }

    if (rock && paper && scissor) {
        console.log("All three found: rock, papaer, scissor found")
    }

    if (rock) {

        console.log(rock.innerHTML)
        rock.addEventListener('click', async function () {
            rockItem.style.backgroundColor = 'yellow';
            paperItem.style.backgroundColor = 'white';
            scissorItem.style.backgroundColor = 'white';
            let { bot, message } = await send_item_to_ai('rock')
            text_rock.innerHTML = message
            ai_rock.innerHTML = bot

        })
    }
    if (paper) {
        console.log(paper.innerHTML)
        paper.addEventListener('click', async function () {
            rockItem.style.backgroundColor = 'white';
            paperItem.style.backgroundColor = 'yellow';
            scissorItem.style.backgroundColor = 'white';
            let { bot, message } = await send_item_to_ai('paper')
            text_rock.innerHTML = message
            ai_rock.innerHTML = bot

        })
    }

    if (scissor) {
        console.log(scissor.innerHTML)
        scissor.addEventListener('click', async function () {
            rockItem.style.backgroundColor = 'white';
            paperItem.style.backgroundColor = 'white';
            scissorItem.style.backgroundColor = 'yellow';
            let { bot, message } = await send_item_to_ai('scissor')
            text_rock.innerHTML = message
            ai_rock.innerHTML = bot

        })
    }

})

async function send_item_to_ai(item) {
    try {
        let response = await fetch('/api/rock_paper_scissor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'item': item })
        });
        let data = await response.json();
        console.log(data);
        return {
            bot: data.bot_item,
            message: data.message
        }
    } catch (error) {
        console.error("AI didn't chose anything");
    }
}