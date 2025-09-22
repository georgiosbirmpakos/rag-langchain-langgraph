// Custom hook for scroll-to-bottom functionality
// This handles the scroll behavior and button visibility logic

import { useState, useEffect, useCallback, useRef } from 'react';

interface UseScrollToBottomOptions {
  threshold?: number; // Distance from bottom to consider "near bottom"
}

export function useScrollToBottom(options: UseScrollToBottomOptions = {}) {
  const { threshold = 100 } = options;
  const [isNearBottom, setIsNearBottom] = useState(true);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Check if user is near the bottom of the scroll container
  const checkIfNearBottom = useCallback(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const distanceFromBottom = 
      container.scrollHeight - container.scrollTop - container.clientHeight;
    
    const nearBottom = distanceFromBottom < threshold;
    setIsNearBottom(nearBottom);
    setShowScrollButton(!nearBottom);
  }, [threshold]);

  // Scroll to bottom function
  const scrollToBottom = useCallback(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    // Check if scrollTo is available (for test environments)
    if (typeof container.scrollTo === 'function') {
      container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth'
      });
    } else {
      // Fallback for test environments
      container.scrollTop = container.scrollHeight;
    }
  }, []);

  // Set up scroll event listener
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    // Initial check
    checkIfNearBottom();

    // Add scroll listener
    container.addEventListener('scroll', checkIfNearBottom, { passive: true });

    // Cleanup
    return () => {
      container.removeEventListener('scroll', checkIfNearBottom);
    };
  }, [checkIfNearBottom]);

  // Auto-scroll when new content is added (if user was near bottom)
  const autoScrollIfNeeded = useCallback(() => {
    if (isNearBottom) {
      // Use setTimeout to ensure DOM has updated
      setTimeout(scrollToBottom, 100);
    }
  }, [isNearBottom, scrollToBottom]);

  return {
    scrollContainerRef,
    isNearBottom,
    showScrollButton,
    scrollToBottom,
    autoScrollIfNeeded,
  };
}
