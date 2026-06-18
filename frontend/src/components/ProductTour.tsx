"use client";

import React, { useState, useEffect } from 'react';
import { Joyride, Step, STATUS } from 'react-joyride';

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
      content: 'This is the top vendor based on the math.',
      skipBeacon: true,
      placement: 'bottom',
    },
    {
      target: '.tour-step-sliders',
      content: 'Use these sliders to adjust your priorities. The scores update instantly.',
      skipBeacon: true,
      placement: 'bottom',
    },
    {
      target: '.tour-step-badges',
      content: 'Quick overview of potential savings, risks, and extraction confidence.',
      skipBeacon: true,
      placement: 'bottom',
    },
    {
      target: '.tour-step-matrix',
      content: 'Compare the vendors side-by-side here.',
      skipBeacon: true,
      placement: 'top',
    },
    {
      target: '.tour-step-confidence',
      content: 'These bars show how confident the AI was when reading the document. Green means high confidence, red means you should verify the value manually.',
      skipBeacon: true,
      skipScroll: true,
      placement: 'top',
    },
    {
      target: '.tour-step-copilot',
      content: 'You can ask questions or test negotiation strategies with the Copilot here.',
      skipBeacon: true,
      placement: 'left',
    }
  ];

  const handleJoyrideEvent = (data: any) => {
    const { status, type } = data;
    // STATUS.FINISHED and STATUS.SKIPPED are valid in v3
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
      options={{
        buttons: ['skip', 'back', 'close', 'primary'], // adds skip button!
        showProgress: true,
        overlayClickAction: false, // prevents closing on overlay click
        primaryColor: '#2563eb',
        zIndex: 10000,
      }}
      locale={{ skip: 'Skip Tour' }}
      onEvent={handleJoyrideEvent}
    />
  );
}
