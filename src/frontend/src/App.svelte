<script>
    import ImageEditor from "./ImageEditor.svelte";

    let counter = -1;
    /**
     * @type {string | null}
     */
    let prediction = null;

    let image = new Image();

    function decrementCounter() {
        if (counter > -1) {
            counter--;
        }

        if (counter == 0) {
            fetch("/api/", {
                method: "post",
                body: JSON.stringify({
                    image: image.src.replace("data:image/png;base64,", ""),
                }),
            })
                .then((res) => res.json())
                .then((json) => (prediction = json.prediction));
        }

        setTimeout(decrementCounter, 10);
    }

    decrementCounter();
</script>

<main class="dark bg-neutral-900 text-white w-screen min-h-screen max-w-screen">
    <div class="flex flex-col justify-center items-center w-full">
        <div class="text-7xl font-bold mt-8">
            {@html prediction ?? "&nbsp;"}
        </div>
        <ImageEditor
            resizedImage={image}
            onDraw={() => {
                counter = 20;
            }}
            onWipe={() => {
                counter = -1;
                prediction = null;
            }}
        />
    </div>
</main>
