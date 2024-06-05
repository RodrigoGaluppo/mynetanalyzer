
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';


ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: '',
    },
  },
};


export default function BarChart({
  labels,data
}:{labels:string[],data:number[]}){
    return (
      <Bar
      data={
        {
          labels,
          datasets: [
            {
              label: '',
              data,
              backgroundColor: [
                "#F56565",
                "#ECC94B",
                "#48BB78",
                "#ED64A6",
                "#ED8936",
                "#4299E1"
              ], 
            },
          ]

        }
      }
      options={{
        responsive: true,
      }}
    />
    )
}