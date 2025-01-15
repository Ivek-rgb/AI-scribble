<script>
    import Combobox from "$lib/components/ui/combobox/combobox.svelte";
    import ImageEditor from "./ImageEditor.svelte";

    let counter = -1;
    /**
     * @type {string | null}
     */
    let prediction = $state(null);

    let imageToSend = $state(new Image());
    let imageSrc = $state("");
    let selectedModel = $state("");

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
                .then((json) => (prediction = json.prediction ?? null));
        }

        setTimeout(decrementCounter, 100);
    }

    decrementCounter();
</script>

<main class="bg-neutral-900 text-white w-screen min-h-screen max-w-screen">
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
        >
            {#snippet children({ params })}
                <Combobox
                    options={[
                        {
                            value: "1",
                            label: "Znam da dugacak tekst overflowa, budem slozio",
                        },
                    ]}
                    bind:value={selectedModel}
                />
            {/snippet}
        </ImageEditor>
    </div>

    Slika koja se šalje:
    <a href={imageSrc} target="_blank">
        <img bind:this={imageToSend} alt="" />
    </a>
</main>
