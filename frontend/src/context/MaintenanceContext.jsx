import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import axios from 'axios';
import { API_BASE_URL } from './AuthContext';
import { Wrench, AlertTriangle, X, ShieldAlert } from 'lucide-react';

export const MaintenanceContext = createContext();

export const MaintenanceProvider = ({ children }) => {
  const [isMaintenanceMode, setIsMaintenanceMode] = useState(false);
  const [maintenanceMessage, setMaintenanceMessage] = useState("The website is temporarily under maintenance. Please try again later.");
  const [maintenanceData, setMaintenanceData] = useState({ enabled_by_admin: '', enabled_at: '' });
  const [isUserPopupOpen, setIsUserPopupOpen] = useState(false);
  const [toggling, setToggling] = useState(false);

  // Fetch current maintenance status from backend
  const checkMaintenanceStatus = useCallback(async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/maintenance/status`);
      if (response.data && response.data.success) {
        setIsMaintenanceMode(!!response.data.maintenance_mode);
        if (response.data.maintenance_message) {
          setMaintenanceMessage(response.data.maintenance_message);
        }
        setMaintenanceData({
          enabled_by_admin: response.data.enabled_by_admin || '',
          enabled_at: response.data.enabled_at || ''
        });
      }
    } catch (err) {
      console.error("[MAINTENANCE] Error fetching status:", err);
    }
  }, []);

  // Initial load & Auto Refresh every 30 seconds
  useEffect(() => {
    checkMaintenanceStatus();
    const interval = setInterval(() => {
      checkMaintenanceStatus();
    }, 30000); // 30 seconds auto-refresh requirement

    return () => clearInterval(interval);
  }, [checkMaintenanceStatus]);

  // Global Axios Interceptor to catch HTTP 503 maintenance responses
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 503) {
          if (error.response.data && error.response.data.maintenance) {
            setIsMaintenanceMode(true);
            if (error.response.data.message) {
              setMaintenanceMessage(error.response.data.message);
            }
            setIsUserPopupOpen(true);
          }
        }
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  // Admin function to toggle maintenance mode
  const toggleMaintenanceMode = async (enableMode, customMessage = "") => {
    setToggling(true);
    try {
      const token = localStorage.getItem('bb_token') || localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/maintenance/toggle`,
        {
          maintenance_mode: enableMode,
          maintenance_message: customMessage || "The website is temporarily under maintenance. Please try again later."
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (response.data && response.data.success) {
        setIsMaintenanceMode(response.data.maintenance_mode);
        setMaintenanceMessage(response.data.maintenance_message);
        setMaintenanceData({
          enabled_by_admin: response.data.enabled_by_admin,
          enabled_at: response.data.enabled_at
        });
        setToggling(false);
        return { success: true, message: response.data.message };
      } else {
        setToggling(false);
        return { success: false, message: response.data.message || "Failed to update maintenance mode." };
      }
    } catch (err) {
      setToggling(false);
      const msg = err.response?.data?.message || err.message || "Failed to toggle maintenance mode.";
      return { success: false, message: msg };
    }
  };

  const showMaintenancePopup = () => {
    setIsUserPopupOpen(true);
  };

  const closeMaintenancePopup = () => {
    setIsUserPopupOpen(false);
  };

  return (
    <MaintenanceContext.Provider
      value={{
        isMaintenanceMode,
        maintenanceMessage,
        maintenanceData,
        toggling,
        toggleMaintenanceMode,
        checkMaintenanceStatus,
        showMaintenancePopup,
        closeMaintenancePopup
      }}
    >
      {children}

      {/* Customer-Facing Website Under Maintenance Popup Modal */}
      {isUserPopupOpen && (
        <div className="fixed inset-0 z-[10000] flex items-center justify-center bg-black/75 backdrop-blur-md p-4 animate-fade-in">
          <div className="relative w-full max-w-md bg-white dark:bg-slate-900 border border-amber-500/30 dark:border-amber-500/40 rounded-3xl overflow-hidden shadow-[0_25px_70px_rgba(0,0,0,0.5)] transform transition-all animate-scale-up">
            
            {/* Header Close Icon */}
            <button
              onClick={closeMaintenancePopup}
              className="absolute top-3 right-3 z-20 text-white bg-black/40 hover:bg-black/60 backdrop-blur-md p-1.5 rounded-full transition-colors cursor-pointer"
              title="Close"
            >
              <X className="h-5 w-5" />
            </button>

            {/* Full-Width Top Hero Banner Image */}
            <div className="relative w-full h-[180px] sm:h-[210px] md:h-[230px] bg-slate-950 overflow-hidden">
              <img
                src="/maintenance_logo.jpg"
                alt="Website Maintenance Hero Banner"
                className="w-full h-full object-cover rounded-t-3xl block select-none no-zoom"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-white dark:from-slate-900 via-transparent to-black/20 pointer-events-none" />
            </div>

            {/* Popup Body Content */}
            <div className="p-6 sm:p-8 text-center">
              {/* Popup Title */}
              <h3 className="text-xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-3">
                Website Under Maintenance
              </h3>

              {/* Popup Message */}
              <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-medium mb-6">
                We are fixing the issue. Please try again shortly.
              </p>

              {/* Information Notice Pill */}
              <div className="bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900/50 rounded-xl p-3.5 mb-6 text-left flex items-start gap-2.5">
                <Wrench className="h-4 w-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                <p className="text-xs text-amber-800 dark:text-amber-300 font-semibold leading-snug">
                  Product browsing remains fully accessible. You can continue exploring our collections.
                </p>
              </div>

              {/* Action Button */}
              <button
                onClick={closeMaintenancePopup}
                className="w-full py-3 px-6 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-white font-bold rounded-2xl shadow-lg shadow-amber-500/25 active:scale-98 transition-all text-sm tracking-wide cursor-pointer"
              >
                Understood & Close
              </button>
            </div>
          </div>
        </div>
      )}
    </MaintenanceContext.Provider>
  );
};

export const useMaintenance = () => {
  const context = useContext(MaintenanceContext);
  if (!context) {
    throw new Error("useMaintenance must be used within a MaintenanceProvider");
  }
  return context;
};
