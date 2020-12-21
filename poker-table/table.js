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
        player_playing: -1,
        players: [
            { name: 'rivy33', color: '#3D9970', stack: 100, onTable: 77, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'kattar', color: '#0074D9', stack: 100, onTable: 23, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'mikelaire', color: 'lightcoral', stack: 100, onTable: 39, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'tomtom', color: '#001f3f', stack: 100, onTable: 21, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'nana', color: '#39CCCC', stack: 100, onTable: 20, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'ionion', color: '#F012BE', stack: 100, onTable: 20, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'link6996', color: '#FF851B', stack: 100, onTable: 20, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'gossboganon', color: '#FF4136', stack: 100, onTable: 88, hasCards: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] }
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

// change player color by clicking on their name plate
function togglePlayer(playerNum) {
    const player = app.players[playerNum - 1];
    player.hasCards = !player.hasCards;
    updatePlayerColors();
}

// add the on click event listener to each player
for (let i = 1; i <= app.players.length; i++) {
    const icon = document.querySelector(`.player-${i}`).querySelector('.avatar');
    icon.addEventListener('click', function () { togglePlayer(i) });
}

// function to refresh the page 
function refreshPage() {
    location.reload();
}