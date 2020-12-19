Vue.component('card', {
    template: `<div class="card" :class="['figures-' + card.f, 'values-' + card.v]">
		<h1>{{card.v}}</h1>
		<div class="figures" :class="card.f"></div>
		<h1>{{card.v}}</h1>
	</div>`,
    props: ['card']
})

let app = new Vue({
    el: '.vue-container',
    data: {
        player_playing: 0,
        players: [
            { name: 'rivy33', bank: 100, onTable: 77, hasCards: false },
            { name: 'kattar', color: 'cyan', bank: 100, onTable: 20, hasCards: true },
            { name: 'mikelaire', color: 'lightcoral', bank: 100, onTable: 20, hasCards: false },
            { name: 'tomtom', color: 'crimson', bank: 100, onTable: 20, hasCards: true },
            { name: 'nana', color: '#444', bank: 100, onTable: 20, hasCards: true },
            { name: 'ionion', color: 'forestgreen', bank: 100, onTable: 20, hasCards: false },
            { name: 'link6996', color: 'goldenrod', bank: 100, onTable: 20, hasCards: false },
            { name: 'gossboganon', color: 'gold', bank: 100, onTable: 20, hasCards: false }
        ],
        figures: [
            'S',
            'H',
            'C',
            'D'
        ],
        values: [
            'A',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            'J',
            'Q',
            'K'
        ]
    },
    computed: {
        cards() {
            let all = []
            for (let figure of this.figures) {
                for (let value of this.values) {
                    all.push({
                        f: figure,
                        v: value
                    })
                }
            }
            return all
        },
        five_cards() {
            let fives = []
            for (let i = 0; i < 5; i++) {
                let rand_id = parseInt(Math.random() * this.cards.length)
                fives.push(this.cards[rand_id])
            }
            return fives
        }
    }
})

// My js additions

// turn players grey if they don't have cards
function updatePlayerColors() {
    for (let i = 1; i <= app.players.length; i++) {
        const p = app.players[i - 1];
        const icon = document.querySelector(`.player-${i}`).querySelector('.avatar');
        if (p.hasCards) {
            icon.style.backgroundColor = p.color || 'dodgerblue';
        }
        else {
            icon.style.backgroundColor = 'grey';
        }
    }
}

updatePlayerColors();

for (let i = 1; i <= app.players.length; i++) {
    const icon = document.querySelector(`.player-${i}`).querySelector('.avatar');
    icon.addEventListener('click', function () { togglePlayer(i) });
}

function refreshPage() {
    location.reload();
}

function togglePlayer(playerNum) {
    console.log(`You clicked on player ${playerNum}`);
    const player = app.players[playerNum - 1];
    player.hasCards = !player.hasCards;
    updatePlayerColors();
}