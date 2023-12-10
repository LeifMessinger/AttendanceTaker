// Timer Web Component
class TimerComponent extends HTMLElement {
	constructor() {
		super();

		this.attachShadow({ mode: 'open' });

		this.shadowRoot.innerHTML = `
			<style>
				:host {
					display: flex;
					flex-direction: column;
					align-items: center;
					justify-content: center;
					width: 200px;
					height: 150px;
					box-sizing: border-box;
					margin: 0 auto 0 auto;
				}

				#timer-container {
					display: flex;
					flex-direction: column;
					align-items: center;
					width: 100%;
					height: 100%;
					background-color: #f0f0f0;
					border: 2px solid #ccc;
					padding: 10px;
					box-sizing: border-box;
				}

				#time-remaining {
					font-size: 4em;
					color: black;
					flex-grow: 1;
				}

				#control-buttons {
					display: flex;
					justify-content: space-around;
					align-items: center;
					width: 100%;
					height: 50%;
				}

				button {
					font-size: 1.5em;
					padding: 10px;
				}

				#play-pause {
					color: green;
				}

				#play-pause.playing {
					color: red;
				}
			</style>

			<div id="timer-container">
				<div id="time-remaining">5:00</div>
				<div id="control-buttons">
					<button id="minus" aria-label="Decrease Timer">-</button>
					<button id="play-pause" class="playing" aria-label="Restart Timer">▶️</button>
					<button id="plus" aria-label="Increase Timer">+</button>
				</div>
			</div>
		`;

		this.timeRemainingElement = this.shadowRoot.getElementById('time-remaining');
		this.playPauseButton = this.shadowRoot.getElementById('play-pause');
		this.minusButton = this.shadowRoot.getElementById('minus');
		this.plusButton = this.shadowRoot.getElementById('plus');

		this.timer = null;
		this.timeRemaining = 300; // 5 minutes in seconds
		this.isPlaying = false;

		this.updateDisplay();
		this.setupEventListeners();
	}

	updateDisplay() {
		const minutes = Math.floor(this.timeRemaining / 60);
		const seconds = this.timeRemaining % 60;
		this.timeRemainingElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
	}

	restartTimer() {
		clearInterval(this.timer);
		this.timeRemaining = 300;
		this.isPlaying = false;
		this.playPauseButton.classList.remove('playing');
		this.updateDisplay();
	}

	togglePlayPause() {
		if (this.isPlaying) {
			this.restartTimer();
		} else {
			this.isPlaying = true;
			this.playPauseButton.classList.add('playing');
			this.updateDisplay();

			this.timer = setInterval(() => {
				this.timeRemaining--;

				if (this.timeRemaining <= 0) {
					this.restartTimer();
					this.timeRemainingElement.style.color = 'red';
				}

				this.updateDisplay();
			}, 1000);
		}
		this.playPauseButton.textContent = this.isPlaying ? '🔄' : '▶️';
	}

	adjustTime(adjustment) {
		if (!this.isPlaying) {
			this.timeRemaining += adjustment;
			this.timeRemaining = Math.max(this.timeRemaining, 0);
			this.updateDisplay();
		}
	}

	setupEventListeners() {
		this.playPauseButton.addEventListener('click', this.togglePlayPause.bind(this));
		this.minusButton.addEventListener('click', () => this.adjustTime(-60));
		this.plusButton.addEventListener('click', () => this.adjustTime(60));
	}

	connectedCallback() {
		this.updateDisplay();
	}
}

// Define the custom element
customElements.define('timer-component', TimerComponent);
