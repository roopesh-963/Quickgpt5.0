import React, { useState, useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import Sidebar from "./components/Sidebar.jsx";
import Chatbox from "./components/Chatbox.jsx";
import Credits from "./pages/Credits.jsx";
import Community from "./pages/Community.jsx";
import Loading from "./pages/Loading.jsx";
import Login from "./pages/Login.jsx";
import { assets } from "./assets/assets";
import { useAppContext } from "./context/AppContext.jsx";
import './assets/prism.css';

const App = () => {
  const { user, loadingUser } = useAppContext();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { pathname } = useLocation();

  // 1. Loading State: Prevents UI flicker while checking authentication
  if (loadingUser || pathname === '/loading' || loadingUser) 
    return <Loading />
  

  // 2. Body Scroll Lock: Prevents scrolling when mobile sidebar is open
 

  return (
    <>
      <Toaster  />

      {user ? (
        <div className="flex h-screen w-screen bg-gradient-to-b from-[#f7f3ff] to-[#e9ddff] text-black transition-colors duration-300 dark:from-[#0f0f0f] dark:to-[#000000]">
          
          {/* Mobile Menu Icon */}
          {!isMenuOpen && (
            <img
              src={assets.menu_icon}
              className="fixed top-3 left-3 w-8 h-8 cursor-pointer md:hidden z-50 dark:invert"
              onClick={() => setIsMenuOpen(true)}
              alt="Open menu"
            />
          )}

          {/* Mobile Overlay */}
          {isMenuOpen && (
            <div
              onClick={() => setIsMenuOpen(false)}
              className="fixed inset-0 bg-black/40 z-40 md:hidden backdrop-blur-sm"
            />
          )}

          {/* Sidebar */}
          <Sidebar isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} />

          {/* Main Content Area */}
          <main className="relative flex-1 h-screen overflow-hidden bg-white/40 dark:bg-black/40 backdrop-blur-xl">
            <Routes>
              <Route path="/" element={<Chatbox />} />
              <Route path="/credits" element={<Credits />} />
              <Route path="/community" element={<Community />} />
            </Routes>
          </main>
        </div>
      ) : (
        // 3. Login Screen: Rendered if no user is authenticated
        <div className="bg-gradient-to-b from-[#242124] to-[#000000] flex items-center justify-center h-screen w-screen">
          <Login />
        </div>
      )}
    </>
  );
};

export default App;