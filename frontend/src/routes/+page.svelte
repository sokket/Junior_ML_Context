<script lang="ts">
	import { browser } from '$app/environment';

	let isRecording: boolean = false;
	let mediaRecorder: MediaRecorder;
	let audioChunks: Blob[] = [];

	async function toggleRecording(): Promise<void> {
		if (isRecording) {
			// Останавливаем запись
			mediaRecorder.stop();
		} else {
			// Начинаем запись
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
			mediaRecorder = new MediaRecorder(stream);

			mediaRecorder.ondataavailable = (event: BlobEvent) => {
				audioChunks.push(event.data);
			};

			mediaRecorder.onstop = async () => {
				const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
				const audioUrl = URL.createObjectURL(audioBlob);
				const audio = new Audio(audioUrl);
				audio.play();

				const formData = new FormData();
				formData.append('audio', audioBlob, 'audio.wav');

				try {
					const response = await fetch('/api/upload/', {
						method: 'POST',
						body: formData
					});

					if (!response.ok) {
						throw new Error('Network response was not ok.');
					}

					const result = await response.json();
					console.log(result);
				} catch (error) {
					console.error('Error:', error);
				}

				// Сбрасываем записанные аудиоданные
				audioChunks = [];
			};

			mediaRecorder.start();
		}

		isRecording = !isRecording;
	}

	function getRandomElement<T>(arr: T[]): T | undefined {
		if (arr.length === 0) {
			return undefined;
		}
		const randomIndex = Math.floor(Math.random() * arr.length);
		return arr[randomIndex];
	}

	let word = { word: '' };

	if (browser) {
		fetch('/api/words/')
			.then((it) => it.json())
			.then((it) => {
				word = getRandomElement(it)!!;
			});
	}
</script>

<div class="page">
	<div class="word">{word.word}</div>
	<button class="button" on:click={toggleRecording}>
		{isRecording ? 'STOP' : 'REC'}
	</button>
</div>

<style>
	.page {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100vh;
		margin: 0;
		background-color: #f5f5f5;
		text-align: center;
	}

	.word {
		font-size: 3rem;
		color: #333;
		margin-bottom: 20px;
	}

	.button {
		margin: 0;
		padding: 0;
		background-color: #d11414;
		border: none;
		color: white;
		width: 64px;
		height: 64px;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		cursor: pointer;
		border-radius: 50%;
		font-size: 16px;
		font-family: 'IBM Plex Sans', sans-serif;
	}

	.button:hover {
		background-color: rgb(65, 72, 65);
	}
</style>
