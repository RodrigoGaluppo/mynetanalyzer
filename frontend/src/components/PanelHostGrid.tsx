import { Center, Heading, Icon, SimpleGrid, Stat, StatArrow, StatGroup, StatHelpText, StatLabel, StatNumber, useColorModeValue,Text } from "@chakra-ui/react";
import { FaBook, FaDatabase, FaNewspaper } from "react-icons/fa";
import {BiBox } from "react-icons/bi";
import { socket,api } from "../services/apiClient";
import { io } from "socket.io-client";
import { useEffect, useState } from "react";
import React from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../hooks/AuthContext";

interface Host{
  id:number;
  name:string;
  created_at:string;
  ip:string;
}

export default function PanelHostGrid() {


   const {ip} = useParams() 
  
    const [packetTransmitted24H, setPacketTransmitted24H] = useState(0)
    const [totalPacketCount24H, settotalPacketCount24H] = useState(0)
    const [Hosts,setHosts] = useState({} as Host[])
    const {token} = useAuth()

   useEffect(()=>{
    api.get("hosts",{ headers: {"Authorization" : `Bearer ${token}`}})
    .then((res)=>{
      setHosts(
        res.data
      )
    })
    .catch((err)=>{
      console.log(err)
    })
   },[])

    // Function to fetch data
    function fetchData() {
      
      socket.emit('request_data_24_hours_sum_host', {ip})
      socket.emit('request_data_24_hours_total_packet_count_host', {ip})
      
      }

    useEffect(() => {
      //Implementing the setInterval method
      const interval = setInterval(fetchData, 5000);

      //Clearing the interval
      return () => clearInterval(interval);
    }, []);


    socket.on('data_update_24_hour_sum_host', function(data) {
        
        data = JSON.parse(data)

        setPacketTransmitted24H(data.value)
    });

    socket.on('data_update_last_24_hours_total_packet_count_host', function(data) {
        
      data = JSON.parse(data)

      settotalPacketCount24H(data.value)
  });

  return (
    
      <SimpleGrid minChildWidth='300px' spacing={4}>
        <Center 
          bg={useColorModeValue("pink.200","gray.900")}
          p="4" py="10" border="0.5px solid #ccc"
        >
          
          <StatGroup   >
            <Stat w="100%" >
                <StatLabel fontSize={"3xl"} > Host: {
                 " " + ip } 
                 <Icon as={BiBox} ml="2" fontSize={"2xl"} /> 
                </StatLabel>
                
               
            </Stat>
            </StatGroup>
          
        </Center>
        <Center 
          bg={useColorModeValue("pink.200","gray.900")}
          p="4" py="10"
        >
          <Heading fontSize={"3xl"} >{packetTransmitted24H} MB  <Text fontSize={"small"}>last 24 hours</Text></Heading>
          <Icon as={FaDatabase} ml="2" fontSize={"2xl"} /> 
          
          
        </Center>
        <Center 
          bg={useColorModeValue("pink.200","gray.900")}
          p="4" py="6"
        >
            
            <Heading fontSize={"3xl"} >{Math.round(totalPacketCount24H / 1024)}k packets <Text fontSize={"small"}>last 24 hours</Text></Heading>
          <Icon as={FaNewspaper} ml="2" fontSize={"2xl"} /> 
          
          
        </Center>

        
        
      </SimpleGrid>
    
  );
}