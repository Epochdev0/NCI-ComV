import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';

interface ParameterSliderProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step: number;
  unit: string;
  icon: string;
}

export const ParameterSlider = ({
  label,
  value,
  onChange,
  min,
  max,
  step,
  unit,
  icon
}: ParameterSliderProps) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <Label className="text-base font-medium flex items-center gap-2">
          <span className="text-xl">{icon}</span>
          {label}
        </Label>
        <span className="text-primary font-mono font-semibold">
          {value.toFixed(step < 1 ? 4 : 1)} {unit}
        </span>
      </div>
      <Slider
        value={[value]}
        onValueChange={(vals) => onChange(vals[0])}
        min={min}
        max={max}
        step={step}
        className="transition-smooth"
      />
    </div>
  );
};
