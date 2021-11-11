import { useEffect, useRef } from "react";

export function useInterval(callback: Function, delay: number) {
	const savedCallback = useRef<Function | null>(null);

	// Remember the latest callback
	useEffect(() => {
		savedCallback.current = callback;
	}, [callback]);

	// Set up the interval
	useEffect(() => {
		function tick() {
			savedCallback.current && savedCallback.current();
		}
		if (delay !== null) {
			tick();
			let id = setInterval(tick, delay);
			return () => clearInterval(id);
		}
	}, [delay]);
}