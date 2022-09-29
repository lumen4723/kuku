<script>
	let currId = 0;
	var images = [
		'https://via.placeholder.com/800x200/200',
		'https://via.placeholder.com/800x200/400',
		'https://via.placeholder.com/800x200/600',
		'https://via.placeholder.com/800x200/800',
		'https://via.placeholder.com/800x200/1000'
	];
	const imgLen = images.length;
	let positionLeft = 0;
	let positionMove_const = 100;

	const moveSlider = () => {
		positionLeft = currId * positionMove_const;
	};

	const next = () => {
		currId = currId >= imgLen - 1 ? 0 : currId + 1;
		moveSlider();
	};

	const prev = () => {
		currId = currId <= 0 ? imgLen - 1 : currId - 1;
		moveSlider();
	};

	const getIndex = (index) => {
		currId = index;
		moveSlider();
	};

	let interval = setInterval(next, 3000);

	const autoPlay = () => {
		interval = setInterval(next, 3000);
	};

	const stopPlay = () => {
		clearInterval(interval);
	};
</script>

<div class="columns">
	<div class="column">
		<div
		class="box"
		style="width: 86%;
        margin: 0 auto;
        border-radius: 10px;
        height: {positionMove_const}%;
        padding: 0.9rem 1.2rem;"
		>
			<!-- svelte-ignore a11y-mouse-events-have-key-events -->
			<div
				class="columns"
				style="margin: auto"
				on:mouseover={stopPlay}
				on:mouseleave={autoPlay}
			>
				<div class="column" id="arrow">
					<img on:click={prev} class="arrowbutton" src="https://via.placeholder.com/30x30/aa6600" alt=""/>
				</div>
				<div class="column" id="contain1">
					<div class="slider" style="left: -{positionLeft}%;">
						{#each images as img}
							<img src={img} alt="" style="width:{positionMove_const}%;" />
						{/each}
					</div>
				</div>
				<div class="column" id="arrow">
					<img on:click={next} class="arrowbutton" src="https://via.placeholder.com/30x30/66aa00" alt=""/>
				</div>
			</div>
			<div class="buttons has-addons is-centered">
				{#each images as _, i}
					<button
						class="button
                    {currId === i ? 'is-danger is-active' : 'is-light'}
                    "
						style="border-radius: 50%;
                    height: 0.4rem;
                    padding: 0.4rem;
                    margin: 0.2rem;
                    "
						on:click={() => getIndex(i)}
					/>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	#contain1 {
		padding: 0px 0px;
		overflow: hidden;
	}
	.slider {
		display: flex;
		align-items: center;
		position: relative;
		transition: left 0.5s;
	}
	.slider img {
		display: flex;
		align-items: center;
		justify-content: space-between;
		object-fit: cover;
		flex-shrink: 0;
	}
	#arrow {
		width: 30%;
		align-items: center;
		display: flex;
		flex-basis: unset;
		padding-left: 0px;
		padding-right: 0px;
	}
	.arrowbutton {
		width: 100%;
	}
	.column {
		flex-basis: unset;
	}
</style>
