import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { StarField } from '@/components/StarField';
import { ParameterSlider } from '@/components/ParameterSlider';
import { ResultCard } from '@/components/ResultCard';
import { supabase } from '@/integrations/supabase/client';
import { Loader2, Sparkles } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ prediction: number; probability: number } | null>(null);
  
  // Signal parameters
  const [koiPeriod, setKoiPeriod] = useState(15.5);
  const [koiDepth, setKoiDepth] = useState(0.005);
  const [koiDuration, setKoiDuration] = useState(3.2);
  const [koiSteff, setKoiSteff] = useState(5800);

  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      const { data, error } = await supabase.functions.invoke('predict', {
        body: {
          koi_period: koiPeriod,
          koi_depth: koiDepth,
          koi_duration: koiDuration,
          koi_steff: koiSteff,
        },
      });

      if (error) throw error;

      setResult(data);
      
      toast({
        title: 'Analysis Complete',
        description: data.prediction === 1 
          ? '🎉 Exoplanet signature detected!' 
          : 'No exoplanet detected in this signal.',
      });
    } catch (error) {
      console.error('Prediction error:', error);
      toast({
        title: 'Analysis Failed',
        description: 'Could not complete the analysis. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative">
      <StarField />
      
      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent">
            🌌 ExoVision
          </h1>
          <p className="text-xl text-muted-foreground">
            Discover New Worlds Through AI-Powered Signal Analysis
          </p>
          <div className="flex items-center justify-center gap-2 mt-4 text-sm text-muted-foreground">
            <Sparkles className="w-4 h-4 text-primary" />
            <span>Powered by machine learning trained on Kepler space telescope data</span>
          </div>
        </motion.div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* Control Panel */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Card className="p-8 backdrop-blur-sm bg-card/80 border-border glow-cyan">
              <h2 className="text-2xl font-bold mb-6 text-center">
                Telescope Signal Parameters
              </h2>
              
              <div className="space-y-6">
                <ParameterSlider
                  icon="🔄"
                  label="Orbital Period"
                  value={koiPeriod}
                  onChange={setKoiPeriod}
                  min={1}
                  max={500}
                  step={0.1}
                  unit="days"
                />
                
                <ParameterSlider
                  icon="📉"
                  label="Transit Depth"
                  value={koiDepth}
                  onChange={setKoiDepth}
                  min={0.0001}
                  max={0.05}
                  step={0.0001}
                  unit="ratio"
                />
                
                <ParameterSlider
                  icon="⏱️"
                  label="Transit Duration"
                  value={koiDuration}
                  onChange={setKoiDuration}
                  min={0.5}
                  max={15}
                  step={0.1}
                  unit="hours"
                />
                
                <ParameterSlider
                  icon="🌡️"
                  label="Star Temperature"
                  value={koiSteff}
                  onChange={setKoiSteff}
                  min={3000}
                  max={10000}
                  step={100}
                  unit="K"
                />
              </div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="mt-8"
              >
                <Button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="w-full h-14 text-lg font-semibold bg-primary hover:bg-primary/90 text-primary-foreground glow-cyan transition-smooth"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Analyzing Signal...
                    </>
                  ) : (
                    <>
                      🔭 Analyze Signal
                    </>
                  )}
                </Button>
              </motion.div>
            </Card>
          </motion.div>

          {/* Result Card */}
          {result && (
            <ResultCard
              prediction={result.prediction}
              probability={result.probability}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default Index;
