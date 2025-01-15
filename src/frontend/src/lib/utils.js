
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";


/**
 * @param {any[]} inputs
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

/** @param {string} str */
export function prettify(str) {
  return str.replaceAll(/[ _-]/gi, ' ')
    .split(' ')
    .map(s => s.slice(0, 1).toUpperCase() + s.slice(1, s.length))
    .join(' ');
}
