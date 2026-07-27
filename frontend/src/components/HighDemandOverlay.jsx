import React, { useEffect, useRef, useContext } from 'react';
import { useLocation } from 'react-router-dom';
import { useHighDemand } from '../context/HighDemandContext';
import { AuthContext } from '../context/AuthContext';

export const HighDemandOverlay = () => {
  const { isHighDemandMode } = useHighDemand();
  const { user, loginType, isAdmin } = useContext(AuthContext);
  const location = useLocation();
  const videoRef = useRef(null);

  // Determine if current user or route is exempt (Admin authentication or Admin routes)
  const isExemptAdmin = Boolean(
    isAdmin ||
    user?.is_admin ||
    loginType === 'admin' ||
    location.pathname.startsWith('/admin') ||
    location.pathname === '/login'
  );

  const shouldShowOverlay = isHighDemandMode && !isExemptAdmin;

  const attemptPlay = () => {
    if (videoRef.current) {
      videoRef.current.muted = true;
      videoRef.current.defaultMuted = true;
      const playPromise = videoRef.current.play();
      if (playPromise !== undefined) {
        playPromise.catch((err) => {
          console.warn("[HIGH_DEMAND] Video autoplay caught:", err);
        });
      }
    }
  };

  useEffect(() => {
    if (!shouldShowOverlay) return;

    // Prevent background scrolling while overlay is active
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    // Intercept and block keyboard navigation / shortcuts
    const handleKeyDown = (e) => {
      e.preventDefault();
      e.stopPropagation();
      return false;
    };

    // Intercept and block right-click context menu
    const handleContextMenu = (e) => {
      e.preventDefault();
      e.stopPropagation();
      return false;
    };

    // Intercept and block mouse wheel & touch scrolling
    const handleScrollTouch = (e) => {
      e.preventDefault();
      e.stopPropagation();
      return false;
    };

    window.addEventListener('keydown', handleKeyDown, { capture: true });
    window.addEventListener('contextmenu', handleContextMenu, { capture: true });
    window.addEventListener('wheel', handleScrollTouch, { capture: true, passive: false });
    window.addEventListener('touchmove', handleScrollTouch, { capture: true, passive: false });

    // Attempt video play programmatically to ensure autoplay success across all browsers
    attemptPlay();

    return () => {
      document.body.style.overflow = originalOverflow;
      window.removeEventListener('keydown', handleKeyDown, { capture: true });
      window.removeEventListener('contextmenu', handleContextMenu, { capture: true });
      window.removeEventListener('wheel', handleScrollTouch, { capture: true });
      window.removeEventListener('touchmove', handleScrollTouch, { capture: true });
    };
  }, [shouldShowOverlay]);

  if (!shouldShowOverlay) return null;

  const handleContainerTap = (e) => {
    e.preventDefault();
    e.stopPropagation();
    attemptPlay();
  };

  return (
    <div
      tabIndex={-1}
      onClick={handleContainerTap}
      onTouchEnd={handleContainerTap}
      className="fixed inset-0 top-0 left-0 w-screen h-screen z-[999999] bg-black overflow-hidden select-none pointer-events-auto flex items-center justify-center cursor-pointer"
      style={{
        width: '100vw',
        height: '100vh',
        position: 'fixed',
        top: 0,
        left: 0,
        zIndex: 999999
      }}
    >
      <video
        ref={videoRef}
        src="/high_demand.mp4"
        preload="auto"
        autoPlay
        muted
        defaultMuted
        loop
        playsInline
        webkit-playsinline="true"
        disablePictureInPicture
        controls={false}
        onLoadedMetadata={attemptPlay}
        onCanPlay={attemptPlay}
        onLoadedData={attemptPlay}
        className="w-full h-full object-contain md:object-cover block select-none pointer-events-none"
        style={{
          width: '100%',
          height: '100%'
        }}
      />
    </div>
  );
};


