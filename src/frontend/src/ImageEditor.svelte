<script>
    import { Button } from "$lib/components/ui/button";
    import { Checkbox } from "$lib/components/ui/checkbox";
    import { Label } from "$lib/components/ui/label";
    import { RotateCcw } from "lucide-svelte";
    import { onMount } from "svelte";
    /** @typedef {Object} Props
     * @prop {HTMLCanvasElement} [stateCanvas]
     * @prop {HTMLCanvasElement} [targetCanvas]
     * @prop {HTMLImageElement} resizedImage
     * @prop {Number} [scale]
     * @prop {Number} [outputWidth]
     * @prop {()=>void} [onDraw]
     */

    /** @type {Props}*/
    let {
        stateCanvas = $bindable(document.createElement("canvas")),
        targetCanvas = $bindable(document.createElement("canvas")),
        resizedImage = $bindable(),
        outputWidth = 28,
        scale = 10,
        onDraw = () => {},
        onWipe = () => {},
    } = $props();

    let canvasSize = $state({ width: 500, height: 500 });

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

    let originalImage = new Image();

    let previousMousePos = { x: 0, y: 0 };
    let drawing = false;

    /**
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
        drawing = false;
        setTimeout(() => {
            updateTargetCanvas();
        }, 5);
    };

    /** @param {MouseEvent} event */
    function draw(event) {
        if (!drawing) {
            return;
        }

        let currentMousePos = getMousePosition(targetCanvas, event);
        stateContext.beginPath();
        stateContext.lineWidth = Math.ceil(
            stateCanvas.width / resizeCanvas.width,
        );
        stateContext.strokeStyle = "white";
        stateContext.lineCap = "round";

        stateContext.moveTo(previousMousePos.x, previousMousePos.y);
        stateContext.lineTo(currentMousePos.x, currentMousePos.y);
        stateContext.stroke();

        previousMousePos = currentMousePos;
        updateTargetCanvas();

        onDraw();
    }

    function updateTargetCanvas() {
        originalImage.src = stateCanvas.toDataURL();
        targetContext.clearRect(0, 0, targetCanvas.width, targetCanvas.height);

        let resizeContext = resizeCanvas.getContext("2d");
        if (!resizeContext) return;

        resizeContext.clearRect(0, 0, resizeCanvas.width, resizeCanvas.height);
        resizeContext.drawImage(originalImage, 0, 0, 28, 28);
        resizedImage.src = resizeCanvas.toDataURL();

        if (preview) {
            targetContext.imageSmoothingEnabled = false;

            targetContext.drawImage(
                resizedImage,
                0,
                0,
                targetCanvas.width,
                targetCanvas.height,
            );
        } else {
            targetContext.imageSmoothingEnabled = true;
            targetContext.drawImage(
                originalImage,
                0,
                0,
                targetCanvas.width,
                targetCanvas.height,
            );
        }
    }

    function wipe() {
        stateContext.clearRect(0, 0, stateCanvas.width, stateCanvas.height);
        updateTargetCanvas();
        onWipe();
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
            width={canvasSize.width}
            height={canvasSize.height}
            onmousedown={drawStart}
            onmouseup={drawEnd}
            onmouseleave={drawEnd}
            onmousemove={draw}
            class="border border-neutral-500 rounded-md relative"
        >
        </canvas>
    </div>
</div>
