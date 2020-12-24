Vue.component('card', {
    template: `<div class="card" :class="['figures-' + card.f, 'values-' + card.v]">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/82473/bicycle-card.jpg" class="card-cover" v-if=hidden>
		<h1>{{card.v}}</h1>
		<div class="figures" :class="card.f"></div>
		<h1>{{card.v}}</h1>
	</div>`,
    props: ['card', 'hidden']
});

let app = new Vue({
    el: '.vue-container',
    data: {
        pov: [true, true, false, true, false, false, false, false],
        dealer: 1,
        turn: 0,
        players: [
            { name: 'rivy33', stack: 100, chipsOnTable: 77, is_playing: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'kattar', stack: 100, chipsOnTable: 23, is_playing: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'mikelaire', stack: 100, chipsOnTable: 39, is_playing: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'tomtom', stack: 100, chipsOnTable: 21, is_playing: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'nana', stack: 100, chipsOnTable: 20, is_playing: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'ionion', stack: 100, chipsOnTable: 20, is_playing: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'link6996', stack: 100, chipsOnTable: 20, is_playing: true, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] },
            { name: 'gossboganon', stack: 100, chipsOnTable: 88, is_playing: false, cards: [{ f: 'S', v: 'A' }, { f: 'C', v: 'A' }] }
        ],
        colors: ['#3D9970', '#0074D9', 'lightcoral', '#001f3f', '#39CCCC', '#F012BE', '#FF851B', '#FF4136'],
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
});

// turn players grey if they don't have cards
function updatePlayerColor(i) {
    const p = app.players[i];
    const icon = document.querySelector(`.player-${i + 1}`).querySelector('.avatar');
    if (p.is_playing) {
        icon.style.backgroundColor = app.colors[i];
    }
    else {
        icon.style.backgroundColor = 'grey';
    }
}

// turn all players avatar colors correctly
function updatePlayersColors() {
    for (let i = 0; i < app.players.length; i++) {
        updatePlayerColor(i);
    }
}

// initialize avatar colors
updatePlayersColors();

// change player color by clicking on their name plate and rebind event listeners
function togglePlayer(i) {
    const player = app.players[i];
    player.is_playing = !player.is_playing;
    updatePlayerColor(i);
    app.$nextTick(function () {
        addflipCardsListener(i);
    })
}

// add the on click event listener to each player
for (let i = 0; i < app.players.length; i++) {
    const icon = document.querySelector(`.player-${i + 1}`).querySelector('.avatar');
    icon.addEventListener('click', function () { togglePlayer(i) });
}

// function to refresh the page 
function refreshPage() {
    location.reload();
}

// draggable slider
var rangeSlider = document.getElementById("rs-range-line");
// input text
var betText = document.getElementById("bet-text");

rangeSlider.addEventListener("input", updateTextBox, false);
betText.addEventListener("input", updateRangeSlider, false);

// update text box to match slider
function updateTextBox() {
    betText.value = rangeSlider.value;
}

// update range slider to match text box
function updateRangeSlider() {
    rangeSlider.value = betText.value;
    if (betText.value === "") {
        rangeSlider.value = 0;
    }
}

// hide cards for player i
function flipCards(i) {
    app.$set(app.pov, i, !app.pov[i]);
}

// add flip cards event listener for player i 
function addflipCardsListener(i) {
    const playerHand = document.querySelectorAll(`.player-${i + 1} .card`);
    for (card of playerHand) {
        card.addEventListener("click", function () { flipCards(i) });
    }
}

// add flip cards event listener for all players
function addflipCardsListeners() {
    for (let i = 0; i < app.players.length; i++) {
        addflipCardsListener(i);
    }
}

// initialize all flip cards event listeners
addflipCardsListeners()