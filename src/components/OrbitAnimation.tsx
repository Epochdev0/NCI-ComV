import { motion } from 'framer-motion';

interface OrbitAnimationProps {
  isExoplanet: boolean;
}

export const OrbitAnimation = ({ isExoplanet }: OrbitAnimationProps) => {
  const planetColor = isExoplanet ? 'hsl(var(--success))' : 'hsl(var(--destructive))';
  
  return (
    <div className="relative w-48 h-48 mx-auto my-8">
      {/* Star */}
      <motion.div
        className="absolute top-1/2 left-1/2 w-16 h-16 rounded-full"
        style={{
          background: 'radial-gradient(circle, hsl(45 100% 70%), hsl(30 100% 50%))',
          transform: 'translate(-50%, -50%)',
        }}
        animate={{
          boxShadow: [
            '0 0 20px hsl(45 100% 70%)',
            '0 0 40px hsl(45 100% 70%)',
            '0 0 20px hsl(45 100% 70%)',
          ],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      
      {/* Orbit path */}
      <div className="absolute top-1/2 left-1/2 w-44 h-44 border-2 border-muted rounded-full opacity-30"
        style={{ transform: 'translate(-50%, -50%)' }}
      />
      
      {/* Planet */}
      <motion.div
        className="absolute w-10 h-10 rounded-full"
        style={{
          background: `radial-gradient(circle at 30% 30%, ${planetColor}, ${planetColor}dd)`,
          top: '50%',
          left: '50%',
          originX: 0.5,
          originY: 0.5,
        }}
        animate={{
          rotate: 360,
          x: [0, 88, 0, -88, 0],
          y: [88, 0, -88, 0, 88],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: 'linear',
        }}
      >
        <motion.div
          animate={{
            boxShadow: [
              `0 0 10px ${planetColor}`,
              `0 0 20px ${planetColor}`,
              `0 0 10px ${planetColor}`,
            ],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="w-full h-full rounded-full"
        />
      </motion.div>
    </div>
  );
};
