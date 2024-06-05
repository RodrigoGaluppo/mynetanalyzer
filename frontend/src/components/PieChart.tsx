import React, { useState } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);


export default function DoughnutChart({data,label}:{data:number[], label:string[]}){
  
  return (
    <Doughnut 
    style={{color:"white"}}
    data={
      {
  
        labels: label,
        datasets: [
          {
            label: '#',
            data: data,
            backgroundColor: [
              "#4299E1",
              "#F56565",
              "#ECC94B",
              "#48BB78",
              "#ED64A6",
              "#ED8936"
              
            ],
            
            borderWidth: 1,
          },
        ],
      }

    }/>
  )
}