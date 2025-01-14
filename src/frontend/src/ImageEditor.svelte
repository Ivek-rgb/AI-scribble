<script>
    import { Button } from "$lib/components/ui/button";
    import { Checkbox } from "$lib/components/ui/checkbox";
    import { Label } from "$lib/components/ui/label";
    import { RotateCcw } from "lucide-svelte";
    import { onMount } from "svelte";
    /** @typedef {Object} Props
     * @prop {HTMLCanvasElement} [stateCanvas]
     * @prop {HTMLCanvasElement} [targetCanvas]
     * @prop {HTMLImageElement} [resizedImage]
     * @prop {HTMLImageElement} [stateImage]
     * @prop {Number} [scale]
     * @prop {Number} [outputWidth]
     * @prop {()=>void} [onDraw]
     * @prop {()=>void} [onWipe]
     */

    /** @type {Props}*/
    let {
        stateCanvas = $bindable(document.createElement("canvas")),
        targetCanvas = $bindable(document.createElement("canvas")),
        resizedImage = $bindable(document.createElement("img")),
        stateImage = $bindable(document.createElement("img")),
        outputWidth = 28,
        scale = 10,
        onDraw = () => {},
        onWipe = () => {},
    } = $props();

    let resizeCanvas = document.createElement("canvas");
    resizeCanvas.width = outputWidth;
    resizeCanvas.height = resizeCanvas.width;

    stateCanvas.width = resizeCanvas.width * scale;
    stateCanvas.height = stateCanvas.width;

    let targetWidth = $state(0);
    let targetHeight = $state(0);
    let preview = $state(false);

    /**
     * @type {CanvasRenderingContext2D }
     */
    let targetContext;

    /**
     * @type {CanvasRenderingContext2D }
     */
    let stateContext;

    let previousMousePos = { x: 0, y: 0 };
    let drawing = false;

    /**
     * Maps click on user facing canvas to
     * corresponding coords on state canvas
     *   @param {HTMLCanvasElement} refCanvas
     *   @param {MouseEvent} mouseEvent
     */
    function getMousePosition(refCanvas, mouseEvent) {
        return {
            x:
                Math.floor(
                    (mouseEvent.clientX -
                        refCanvas.getBoundingClientRect().left) *
                        (stateCanvas.width / targetCanvas.width),
                ) + 0.5,
            y:
                Math.floor(
                    (mouseEvent.clientY -
                        refCanvas.getBoundingClientRect().top) *
                        (stateCanvas.width / targetCanvas.width),
                ) + 0.5,
        };
    }

    const drawStart = (/** @type {MouseEvent} */ e) => {
        previousMousePos = getMousePosition(targetCanvas, e);
        drawing = true;
    };
    const drawEnd = (/** @type {MouseEvent} */ e) => {
        draw(e);
        setTimeout(updateTargetCanvas, 5);
        drawing = false;
    };

    /** @param {MouseEvent} event */
    function draw(event) {
        if (!drawing) {
            return;
        }

        let currentMousePos = getMousePosition(targetCanvas, event);
        stateContext.beginPath();
        stateContext.lineWidth =
            Math.ceil(stateCanvas.width / resizeCanvas.width) * 1.5;

        stateContext.moveTo(previousMousePos.x, previousMousePos.y);
        stateContext.lineTo(currentMousePos.x, currentMousePos.y);
        stateContext.stroke();

        previousMousePos = currentMousePos;
        updateTargetCanvas();

        onDraw();
    }

    /**
     * Iz nekog razloga, update na targetCanvas zna kasnit.
     * Ako se na njega naslika nova slika, browser tu sliku
     * nacrta na canvas kad mu se sprdne. Uglavnom instantno,
     * ali zna kasnit koju sekundu. Nisam siguran zasto.
     */
    function updateTargetCanvas() {
        stateImage.src = stateCanvas.toDataURL();

        // Clear user facing canvas
        targetContext.clearRect(0, 0, targetCanvas.width, targetCanvas.height);

        let resizeContext = resizeCanvas.getContext("2d");
        if (!resizeContext) return;

        // Update resized image
        resizeContext.fillRect(0, 0, resizeCanvas.width, resizeCanvas.height);
        resizeContext.drawImage(stateImage, 0, 0, 28, 28);
        resizedImage.src = resizeCanvas.toDataURL();

        if (preview) {
            // Draw scaled down image on user facing canvas
            targetContext.imageSmoothingEnabled = false;

            targetContext.drawImage(
                resizedImage,
                0,
                0,
                targetCanvas.width,
                targetCanvas.height,
            );
        } else {
            // Draw full res image on user facing canvas
            targetContext.imageSmoothingEnabled = true;
            targetContext.drawImage(
                stateImage,
                0,
                0,
                targetCanvas.width,
                targetCanvas.height,
            );
        }
        targetContext.stroke();
    }

    function wipe() {
        stateContext.fillRect(0, 0, stateCanvas.width, stateCanvas.height);
        onWipe();
        updateTargetCanvas();
    }

    // Assign canvas context variables used through component
    onMount(() => {
        targetContext =
            targetCanvas.getContext("2d") ??
            (() => {
                throw Error("Unable to get context");
            })();
        stateContext =
            stateCanvas.getContext("2d") ??
            (() => {
                throw Error("Unable to get context");
            })();

        // Pozadinska boja
        stateContext.fillStyle = "white";

        // Boja broja
        stateContext.strokeStyle = "black";
        stateContext.lineCap = "round";

        stateContext.fillRect(0, 0, stateCanvas.width, stateCanvas.height);
        updateTargetCanvas();
    });

    // Handle window resize
    $effect(() => {
        targetCanvas.width = targetWidth;
        targetCanvas.height = targetWidth;
        updateTargetCanvas();
    });
</script>

<div class="w-full h-fit p-4 max-w-screen-sm relative overflow-clip">
    <div class="flex items-center justify-between mb-4">
        <div>
            <Checkbox id="preview_checkbox" bind:checked={preview} /><Label
                for="preview_checkbox">Preview</Label
            >
        </div>
        <div>
            <Button onclick={wipe}><RotateCcw /></Button>
        </div>
    </div>
    <div class="relative">
        <div
            class="absolute w-full h-full opacity-0 left-0 top-0 mx-4"
            bind:clientWidth={targetWidth}
            bind:clientHeight={targetHeight}
        ></div>
        <canvas
            bind:this={targetCanvas}
            width={targetCanvas.width}
            height={targetCanvas.height}
            onmousedown={drawStart}
            onmouseup={drawEnd}
            onmouseleave={drawEnd}
            onmousemove={draw}
            class="border border-neutral-500 rounded-md relative"
        >
        </canvas>
    </div>
</div>
