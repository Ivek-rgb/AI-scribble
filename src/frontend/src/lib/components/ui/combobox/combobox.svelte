<script lang="ts">
	import Check from "lucide-svelte/icons/check";
	import ChevronsUpDown from "lucide-svelte/icons/chevrons-up-down";
	import { tick } from "svelte";
	import * as Command from "$lib/components/ui/command/index.js";
	import * as Popover from "$lib/components/ui/popover/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { cn } from "$lib/utils.js";
	import { LoaderIcon } from "lucide-svelte";

	let {
		options = $bindable([]),
		placeholder = "Select...",
		onChange = (_: string) => {},
		value = $bindable(""),
		loading = $bindable(false),
	} = $props();

	let open = $state(false);
	let triggerRef = $state<HTMLButtonElement>(null!);

	const selectedValue = $derived(
		options.find((f) => f.value === value)?.label,
	);

	// We want to refocus the trigger button when the user selects
	// an item from the list so users can continue navigating the
	// rest of the form with the keyboard.
	function closeAndFocusTrigger() {
		open = false;
		tick().then(() => {
			triggerRef.focus();
		});
	}
</script>

<Popover.Root bind:open>
	<Popover.Trigger bind:ref={triggerRef}>
		{#snippet child({ props })}
			<Button
				variant="outline"
				class="w-[200px] justify-between pl-2 gap-1"
				{...props}
				role="combobox"
				aria-expanded={open}
			>
				{#if loading}
					<LoaderIcon class="size-4 animate-spin opacity-50" />
				{:else}
					<!-- else content here -->
					<ChevronsUpDown class="mr-1 size-4 shrink-0 opacity-50" />
					<span class="truncate w-full max-w-full">
						{selectedValue || "Select a model..."}
					</span>
				{/if}
			</Button>
		{/snippet}
	</Popover.Trigger>
	<Popover.Content class="sm:w-fit max-w-[400px] p-0">
		<Command.Root>
			<Command.Input {placeholder} />
			<Command.List>
				<Command.Empty>Nothing found.</Command.Empty>
				<Command.Group>
					{#each options as option}
						<Command.Item
							value={option.value}
							class="overflow-clip gap-1"
							onSelect={() => {
								value = option.value;
								onChange(value);
								closeAndFocusTrigger();
							}}
						>
							<Check
								class={cn(
									"mr-1 size-4",
									value !== option.value &&
										"text-transparent",
								)}
							/>
							<span class="truncate">
								{option.label}
							</span>
						</Command.Item>
					{/each}
				</Command.Group>
			</Command.List>
		</Command.Root>
	</Popover.Content>
</Popover.Root>
