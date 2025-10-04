import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { OrbitAnimation } from './OrbitAnimation';
import { Telescope, CheckCircle2, XCircle } from 'lucide-react';

interface ResultCardProps {
  prediction: number;
  probability: number;
}

export const ResultCard = ({ prediction, probability }: ResultCardProps) => {
  const isExoplanet = prediction === 1;
  const percentage = (probability * 100).toFixed(1);
  
  const cardClassName = isExoplanet 
    ? 'border-success glow-success' 
    : 'border-destructive glow-destructive';
  
  const gradientClass = isExoplanet ? 'gradient-detection' : 'gradient-negative';
  
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
    >
      <Card className={`p-8 ${cardClassName} backdrop-blur-sm bg-card/80 transition-smooth`}>
        <div className="text-center space-y-6">
          {/* Icon and Title */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
            className="flex flex-col items-center gap-4"
          >
            {isExoplanet ? (
              <CheckCircle2 className="w-16 h-16 text-success" />
            ) : (
              <XCircle className="w-16 h-16 text-destructive" />
            )}
            
            <h2 className="text-3xl font-bold">
              {isExoplanet ? '✅ Exoplanet Detected!' : '❌ No Planet Detected'}
            </h2>
          </motion.div>
          
          {/* Probability */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className={`inline-block px-6 py-3 rounded-full ${gradientClass} text-background font-bold text-2xl`}
          >
            {percentage}% Confidence
          </motion.div>
          
          {/* Orbit Animation */}
          <OrbitAnimation isExoplanet={isExoplanet} />
          
          {/* Description */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-muted-foreground max-w-md mx-auto"
          >
            {isExoplanet
              ? 'The signal characteristics match exoplanet transit patterns. This could be a new world!'
              : 'The signal does not show typical exoplanet characteristics. This might be stellar noise or instrumental artifacts.'}
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="flex items-center justify-center gap-2 text-sm text-muted-foreground"
          >
            <Telescope className="w-4 h-4" />
            <span>Analysis based on Kepler telescope data patterns</span>
          </motion.div>
        </div>
      </Card>
    </motion.div>
  );
};
