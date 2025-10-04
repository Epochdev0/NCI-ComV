import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { koi_period, koi_depth, koi_duration, koi_steff } = await req.json();
    
    console.log('Received prediction request:', { koi_period, koi_depth, koi_duration, koi_steff });

    // ML-inspired prediction logic based on realistic exoplanet characteristics
    // This simulates a trained classifier with weighted features
    
    // Normalize inputs to expected ranges
    const normalizedPeriod = Math.min(koi_period / 500, 1); // 0-500 days typical
    const normalizedDepth = Math.min(koi_depth / 0.01, 1); // 0-1% typical transit depth
    const normalizedDuration = Math.min(koi_duration / 10, 1); // 0-10 hours typical
    const normalizedTemp = Math.min(koi_steff / 10000, 1); // 3000-10000K typical
    
    // Feature scoring (simulating learned weights from training)
    // These weights are inspired by real exoplanet detection patterns
    let score = 0;
    
    // Orbital period sweet spot (3-100 days are most common detections)
    if (koi_period >= 3 && koi_period <= 100) {
      score += 0.25;
    } else if (koi_period > 100 && koi_period <= 300) {
      score += 0.15;
    } else {
      score += 0.05;
    }
    
    // Transit depth (deeper transits = larger planets = easier detection)
    if (koi_depth >= 0.001 && koi_depth <= 0.05) {
      score += 0.30;
      // Bonus for Earth-sized to Jupiter-sized transits
      if (koi_depth >= 0.005 && koi_depth <= 0.02) {
        score += 0.1;
      }
    }
    
    // Transit duration consistency check
    // Realistic transit duration should correlate with period
    const expectedDuration = Math.sqrt(koi_period) * 0.2;
    const durationRatio = Math.abs(koi_duration - expectedDuration) / expectedDuration;
    if (durationRatio < 0.5) {
      score += 0.20;
    } else if (durationRatio < 1.0) {
      score += 0.10;
    }
    
    // Star temperature (solar-type stars most studied)
    if (koi_steff >= 5000 && koi_steff <= 7000) {
      score += 0.15;
    } else if (koi_steff >= 4000 && koi_steff <= 8000) {
      score += 0.08;
    }
    
    // Add some realistic noise/variance
    const noise = (Math.random() - 0.5) * 0.1;
    score = Math.max(0, Math.min(1, score + noise));
    
    // Convert to probability and prediction
    const probability = score;
    const prediction = probability >= 0.5 ? 1 : 0;
    
    console.log('Prediction result:', { prediction, probability: probability.toFixed(4) });
    
    return new Response(
      JSON.stringify({ 
        prediction, 
        probability: parseFloat(probability.toFixed(4))
      }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200 
      }
    );
  } catch (error) {
    console.error('Error in predict function:', error);
    const message = error instanceof Error ? error.message : 'Unknown error occurred';
    return new Response(
      JSON.stringify({ error: message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500
      }
    );
  }
});
