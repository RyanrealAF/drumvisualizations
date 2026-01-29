import React, { useState, useRef, useEffect, useCallback } from 'react';
import DrumOverlay from './DrumOverlay';

// Define global types
type StemName = 'vocals' | 'drums' | 'bass' | 'guitar' | 'piano' | 'other';
type StepId = 1 | 2 | 3 | 4 | 5 | 6;

interface ProgressRingProps {
  progress: number;
}

const ProgressRing: React.FC<ProgressRingProps> = ({ progress }) => {
  const radius = 58;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100 * circumference);

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg className="w-32 h-32">
        <circle className="text-gray-200" strokeWidth="8" stroke="currentColor" fill="transparent" r={radius} cx="64" cy="64"/>
        <circle
          className="text-[#D2643C] progress-ring__circle"
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="64"
          cy="64"
        />
      </svg>
      <span className="absolute text-2xl font-bold text-[#3D3631]">{Math.round(progress)}%</span>
    </div>
  );
};

interface StepIndicatorProps {
  id: StepId;
  label: string;
  isActive: boolean;
}

const StepIndicator: React.FC<StepIndicatorProps> = ({ label, isActive }) => {
  return (
    <div className={`flex items-center gap-3 text-sm transition-colors duration-300 ${isActive ? 'text-[#D2643C] font-bold' : 'text-gray-400'}`}>
      <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-[#D2643C]' : 'bg-current'}`}></div>
      {label}
    </div>
  );
};

interface StemCardProps {
  stem: StemName;
  isActivated: boolean;
}

const StemCard: React.FC<StemCardProps> = ({ stem, isActivated }) => {
  const progressWidth = isActivated ? '100%' : '0%';
  const classes = `stem-card p-4 rounded-xl border bg-white transition-all duration-500 ${
    isActivated
      ? 'opacity-100 shadow-md scale-105 border-[#D2643C]/20'
      : 'opacity-40 border-gray-100'
  }`;

  return (
    <div className={classes} data-stem={stem}>
      <p className="text-xs font-bold text-gray-400 uppercase">{stem.charAt(0).toUpperCase() + stem.slice(1)}</p>
      <div className="h-1 w-full bg-gray-100 mt-2 rounded-full overflow-hidden">
        <div className="h-full bg-[#D2643C] transition-all duration-500" style={{ width: progressWidth }}></div>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string>('No file selected');
  const [progress, setProgress] = useState<number>(0);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<string>('Waiting for Input...');
  const [activeSteps, setActiveSteps] = useState<Set<StepId>>(new Set());
  const [activatedStems, setActivatedStems] = useState<Set<StemName>>(new Set());
  const [wsStatus, setWsStatus] = useState<string>('DISCONNECTED');

  // WebSocket Listener Simulation
  useEffect(() => {
    if (isProcessing) {
        setWsStatus('CONNECTING...');
        const timer = setTimeout(() => {
            setWsStatus('LIVE STREAMING');
        }, 2000);
        return () => clearTimeout(timer);
    } else {
        setWsStatus('DISCONNECTED');
    }
  }, [isProcessing]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const uploadedFile = e.target.files[0];
      setFile(uploadedFile);
      setFileName(uploadedFile.name);
      setStatusMessage('Ready to start');
    }
  };

  const runStep = useCallback(async (id: StepId, msg: string, targetProgress: number) => {
    setStatusMessage(msg);
    setActiveSteps(prev => new Set(prev).add(id));

    const startProgress = progress;
    const diff = targetProgress - startProgress;

    return new Promise<void>(resolve => {
      let current = 0;
      const interval = setInterval(() => {
        current += 1;
        setProgress(startProgress + (current / 100) * diff);
        if (current >= 100) {
          clearInterval(interval);
          resolve();
        }
      }, 15); // Ultra-fast BOLT simulation
    });
  }, [progress]);

  const activateAllStems = useCallback(() => {
    const stems: StemName[] = ['vocals', 'drums', 'bass', 'guitar', 'piano', 'other'];
    stems.forEach((stem, i) => {
      setTimeout(() => {
        setActivatedStems(prev => new Set(prev).add(stem));
      }, i * 100);
    });
  }, []);

  const handleRunSeparation = useCallback(async () => {
    setIsProcessing(true);
    setStatusMessage('Initializing Optimized Environment...');
    setActiveSteps(new Set());
    setActivatedStems(new Set());
    setProgress(0);

    // Optimized High-Fidelity Extraction Pipeline Simulation
    await runStep(1, 'Mounting RAM Buffer (/dev/shm)...', 10);
    await runStep(2, 'RAM-Piped cleaning (FFT Denoise)...', 25);
    await runStep(3, 'Core Separation (Bypassing Disk I/O)...', 65);
    activateAllStems();
    await runStep(4, 'Parallel Refinement (Vocals + Drums)...', 90);
    await runStep(5, 'Validating Optimized Artifacts...', 95);
    await runStep(6, 'Final Signal Audit & Cache Sync...', 100);

    setStatusMessage('Mission Complete. Optimized (⚡ Bolt).');
    setIsProcessing(false);
  }, [runStep, activateAllStems]);


  return (
    <div className="max-w-6xl mx-auto space-y-8 p-4 md:p-8">
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tighter text-[#3D3631] flex items-center">
            DEMUCS <span className="text-[#D2643C] ml-2">6S</span> 
            <span className="text-[10px] bg-[#D2643C] text-white px-2 py-0.5 rounded-sm font-black ml-4 tracking-[0.2em] uppercase">⚡ BOLT ENGINE</span>
          </h1>
          <p className="text-gray-500 font-medium italic mt-1">"Talk street, think prophet. Scars become scripture."</p>
        </div>
        <div className="flex items-center gap-4">
          <input type="file" id="audio-upload" className="hidden" accept="audio/*" onChange={handleFileChange} />
          <button
            onClick={() => document.getElementById('audio-upload')?.click()}
            className="flex items-center gap-2 px-6 py-3 bg-white border-2 border-[#3D3631] rounded-none shadow-[4px_4px_0px_0px_rgba(61,54,49,1)] hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all font-bold uppercase text-xs tracking-widest"
            disabled={isProcessing}
          >
            <span>Select Audio</span>
          </button>
          <button
            onClick={handleRunSeparation}
            disabled={!file || isProcessing}
            className="px-6 py-3 bg-[#3D3631] text-white rounded-none shadow-[4px_4px_0px_0px_rgba(210,100,60,1)] hover:shadow-none hover:translate-x-1 hover:translate-y-1 disabled:opacity-50 disabled:shadow-none transition-all font-bold uppercase text-xs tracking-widest"
          >
            Run Optimized Extraction
          </button>
        </div>
      </header>

      {/* Main Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

        {/* Left Column: Status */}
        <div className="lg:col-span-4 space-y-8">
          <div className="bg-white border-2 border-[#3D3631] p-8 shadow-[8px_8px_0px_0px_rgba(61,54,49,0.1)]">
            <div className="flex justify-between items-center mb-8">
                <h3 className="text-xs font-black text-gray-400 uppercase tracking-[0.2em]">Optimization Profile</h3>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${wsStatus === 'LIVE STREAMING' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                    {wsStatus}
                </span>
            </div>

            <div className="flex flex-col items-center justify-center py-6 border-b border-gray-100 mb-8">
              <ProgressRing progress={progress} />
              <p className={`mt-6 text-xs font-black uppercase tracking-widest text-center ${isProcessing ? 'text-[#D2643C] animate-pulse' : 'text-gray-600'}`}>
                {statusMessage}
              </p>
            </div>

            <div className="space-y-4">
              <StepIndicator id={1} label="RAM Initialization" isActive={activeSteps.has(1)} />
              <StepIndicator id={2} label="Piped Denoising" isActive={activeSteps.has(2)} />
              <StepIndicator id={3} label="CUDA Separation" isActive={activeSteps.has(3)} />
              <StepIndicator id={4} label="Parallel Refinement" isActive={activeSteps.has(4)} />
              <StepIndicator id={5} label="Fast Validation" isActive={activeSteps.has(5)} />
              <StepIndicator id={6} label="Signal Audit" isActive={activeSteps.has(6)} />
            </div>
          </div>

          {file && (
            <div className="bg-[#3D3631] p-6 text-white border-l-8 border-[#D2643C] shadow-lg">
              <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest mb-1">Active Artifact</p>
              <p className="font-mono text-sm truncate opacity-90">{fileName}</p>
            </div>
          )}
        </div>

        {/* Right Column: Visualizer & Stems */}
        <div className="lg:col-span-8 space-y-8">
          {/* Main Visualizer */}
          <DrumOverlay isProcessing={isProcessing || activeSteps.has(6)} />

          {/* Stem Output Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            {['vocals', 'drums', 'bass', 'guitar', 'piano', 'other'].map((stemName) => (
              <StemCard key={stemName} stem={stemName as StemName} isActivated={activatedStems.has(stemName as StemName)} />
            ))}
          </div>
          
          <div className="p-12 bg-[#fdfbf7] border-2 border-dashed border-gray-300 text-center relative overflow-hidden group">
            <div className="absolute inset-0 bg-[#D2643C] opacity-0 group-hover:opacity-5 transition-opacity" />
            <p className="text-sm text-gray-400 font-bold tracking-widest uppercase">Piping optimization reducing I/O latency by ~25%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
