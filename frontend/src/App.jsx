import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Home from "./components/Home";
import AboutUs from "./components/AboutUs";
import Discover from "./components/Discover";
import CheckOptions from "./components/CheckOptions";
import UploadImage from "./components/UploadImage";
import UploadVideo from "./components/UploadVideo";
import UploadText from "./components/UploadText";
import UploadAudio from "./components/UploadAudio";
import UploadFile from "./components/UploadFile";

export default function App() {
  return (
    <Router>
      <Navbar />
      <main className="mt-16 min-h-screen">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/discover" element={<Discover />} />

          <Route path="/check" element={<CheckOptions />} />
          <Route path="/check/image" element={<UploadImage />} />
          <Route path="/check/video" element={<UploadVideo />} />
          <Route path="/check/text" element={<UploadText />} />
          <Route path="/check/audio" element={<UploadAudio />} />
          <Route path="/check/file" element={<UploadFile />} />

          {/* Fallback to homepage for unmatched routes */}
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </Router>
  );
}
