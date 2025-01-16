<script>
    import Combobox from "$lib/components/ui/combobox/combobox.svelte";
    import { onMount } from "svelte";
    import ImageEditor from "./ImageEditor.svelte";
    import { appState } from "$lib/state.svelte";
    import { prettify } from "$lib/utils.js";

    let guess_api_url = "/api/guess";
    let models_api_url = "/api/models";

    let counter = -1;
    /**
     * @type {string}
     */
    let prediction = $state("");

    let imageToSend = $state(new Image());
    let imageSrc = $state("");
    /**
     * @type {Promise<Response>}
     */
    let guessPromise;

    /**
     * @param {string} model_name
     */
    function handleModelChange(model_name) {
        fetch(models_api_url, {
            method: "post",
            body: JSON.stringify({ model_name }),
        })
            .then(() => {
                if (prediction.length) sendForGuess();
            })
            .catch((e) => {
                console.log(e);
                fetchModels();
            });
    }

    function fetchModels() {
        appState.modelsBeingRefreshed = true;
        fetch(models_api_url, {
            method: "get",
        })
            .then((res) => res.json())
            .then((json) => {
                appState.availableModels = json.available_models.map(
                    (/** @type {string} */ model) => ({
                        value: model,
                        label: prettify(model),
                    }),
                );
                appState.loadedModel = json.current_model;
                appState.modelsBeingRefreshed = false;
            })
            .catch(console.log);
    }

    function sendForGuess() {
        const guessUUID = crypto.randomUUID();
        appState.guessPromiseUUID = guessUUID;

        if (!appState.guessing) {
            appState.guessing = true;
            setTimeout(() => {
                if (appState.guessing) prediction = "";
                appendHmms();
            }, 200);
        }

        guessPromise = fetch(guess_api_url, {
            method: "post",
            body: JSON.stringify({
                image: imageToSend.src.replace("data:image/png;base64,", ""),
                compressed: false,
            }),
        });
        guessPromise
            .then((res) =>
                appState.guessPromiseUUID === guessUUID
                    ? res.json()
                    : Promise.reject(),
            )
            .then((json) => {
                prediction = json.prediction ?? "";
                appState.guessing = false;
            })
            .catch(() => {});
    }

    function decrementCounter() {
        if (counter > -1) {
            counter--;
        }

        if (counter == 0) {
            sendForGuess();
        }

        setTimeout(decrementCounter, 100);
    }

    function appendHmms() {
        // 🤔 = 2 bytea
        if (appState.guessing && prediction.length < 8) {
            prediction += "🤔";
            setTimeout(appendHmms, 200);
        }
    }

    onMount(() => {
        fetchModels();
        decrementCounter();
    });
</script>

<svelte:head>
    {#if prediction.length}
        <title>{prettify(prediction)} - AI Scribble</title>
    {:else}
        <title>AI Scribble</title>
    {/if}
</svelte:head>

<main class="bg-neutral-900 text-white w-screen min-h-screen max-w-screen">
    <div class="flex flex-col justify-center items-center w-full">
        <div
            class="flex justify-center items-center h-[70px] md:h-[90px] lg:h-[110px]"
        >
            <div
                data-largetext={prediction?.length > 15}
                class="text-5xl md:text-6xl lg:text-7xl
            data-[largetext=true]:text-4xl
            data-[largetext=true]:md:text-5xl
            data-[largetext=true]:lg:text-6xl
            font-bold mt-8"
            >
                {@html prediction.length ? prettify(prediction) : "&nbsp;"}
            </div>
        </div>
        <ImageEditor
            stateImage={imageToSend}
            onDraw={() => {
                counter = 2;
                imageSrc = imageToSend.src;
            }}
            onWipe={() => {
                counter = -1;
                prediction = "";
            }}
        >
            {#snippet children()}
                <Combobox
                    bind:options={appState.availableModels}
                    onChange={handleModelChange}
                    bind:value={appState.loadedModel}
                    bind:loading={appState.modelsBeingRefreshed}
                />
            {/snippet}
        </ImageEditor>
    </div>
</main>
