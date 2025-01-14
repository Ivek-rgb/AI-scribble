<script>
    import ImageEditor from "./ImageEditor.svelte";

    let counter = -1;
    /**
     * @type {string | null}
     */
    let prediction = $state(null);

    let imageToSend = $state(new Image());
    let imageSrc = $state("");

    function decrementCounter() {
        if (counter > -1) {
            counter--;
        }

        if (counter == 0) {
            fetch("/api/", {
                method: "post",
                body: JSON.stringify({
                    image: imageToSend.src.replace(
                        "data:image/png;base64,",
                        "",
                    ),
                    compressed: false,
                }),
            })
                .then((res) => res.json())
                .then((json) => (prediction = json.prediction));
        }

        setTimeout(decrementCounter, 100);
    }

    decrementCounter();
</script>

<main class="dark bg-neutral-900 text-white w-screen min-h-screen max-w-screen">
    <div class="flex flex-col justify-center items-center w-full">
        <div class="text-7xl font-bold mt-8">
            {@html prediction ?? "&nbsp;"}
        </div>
        <ImageEditor
            stateImage={imageToSend}
            onDraw={() => {
                counter = 2;
                imageSrc = imageToSend.src;
            }}
            onWipe={() => {
                counter = -1;
                prediction = null;
            }}
        />
    </div>

    Slika koja se šalje:
    <a href={imageSrc} target="_blank">
        <img bind:this={imageToSend} alt="" />
    </a>
</main>
