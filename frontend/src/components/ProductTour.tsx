"use client";

import React, { useState, useEffect } from 'react';
import { Joyride, Step, CallBackProps, STATUS } from 'react-joyride';

interface ProductTourProps {
  run: boolean;
}

export function ProductTour({ run }: ProductTourProps) {
  const [hasSeenTour, setHasSeenTour] = useState(false);

  useEffect(() => {
    const seen = localStorage.getItem('hasSeenTour');
    if (seen === 'true') {
      setHasSeenTour(true);
    }
  }, []);

  const steps: Step[] = [
    {
      target: '.tour-step-winner',
      content: 'This is your recommended vendor, calculated using 100% deterministic math.',
      disableBeacon: true,
      placement: 'bottom',
    },
    {
      target: '.tour-step-badges',
      content: 'Quickly see potential savings, risk profile, and the AI\'s overall math confidence at a glance.',
      placement: 'bottom',
    },
    {
      target: '.tour-step-sliders',
      content: 'Try dragging these sliders! The math recalculates instantly on the frontend without calling the AI.',
      placement: 'bottom',
    },
    {
      target: '.tour-step-matrix',
      content: 'Compare all vendors side-by-side cleanly and efficiently.',
      placement: 'top',
    },
    {
      target: '.tour-step-confidence',
      content: 'This is crucial: see exactly how confident the AI was when extracting every single field. No hidden hallucinations. Green is solid, Red needs verification.',
      placement: 'top',
    },
    {
      target: '.tour-step-copilot',
      content: 'Ask questions or simulate negotiations with the AI Copilot on the right.',
      placement: 'left',
    }
  ];

  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status } = data;
    const finishedStatuses: string[] = [STATUS.FINISHED, STATUS.SKIPPED];
    
    if (finishedStatuses.includes(status)) {
      localStorage.setItem('hasSeenTour', 'true');
      setHasSeenTour(true);
    }
  };

  return (
    <Joyride
      steps={steps}
      run={run && !hasSeenTour}
      continuous={true}
      showProgress={true}
      showSkipButton={true}
      callback={handleJoyrideCallback}
      styles={{
        options: {
          primaryColor: '#2563eb', // blue-600 to match our UI
          zIndex: 10000,
        },
      }}
    />
  );
}
