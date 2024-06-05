import { Center, Flex, Grid, GridItem, Heading, Icon, SimpleGrid, useColorModeValue,Text, Box, VStack } from "@chakra-ui/react";
import { FaBook, FaPlay, FaUser } from "react-icons/fa";
import PieChart from "../components/PieChart";
import LineChart from "../components/LineChart";
import PanelHostGrid from "../components/PanelHostGrid";
import SidebarWithHeader from "../components/SideBar";
import { useEffect, useState } from "react";
import {api,socket} from "../services/apiClient";
import { useAuth } from "../hooks/AuthContext";
import BarChart from "../components/BarChart";

import DoughnutChart from "../components/PieChart";
import { useParams } from "react-router-dom";

interface charData{
  data:number[],
  labels:string[]
}

export default function Panel() {
 


  const {token,user} = useAuth()
  
  const {ip} = useParams() 

  const [chart30Data, setChart30Data] = useState({} as charData)
  const [chart60Data, setChart60Data] = useState({} as charData)
  const [chart12HData, setChart12HData] = useState({} as charData)
  const [chart24HData, setChart24HData] = useState({} as charData)

  const [chartprotocolsData, setChartprotocolsData] = useState({} as charData)
  const [chartsourcePortsData, setChartsourcePortsData] = useState({} as charData)
  const [chartDestPortsData, setChartDestPortsData] = useState({} as charData)

  const [chartTopSourceIPs, setChartTopSourceIPs] = useState({} as charData)
  const [chartTopDestinationIPs, setChartTopDestinationIPs] = useState({} as charData)



   // Function to fetch data
   function fetchData() {
    
    socket.emit('request_data_30_host', {ip})
    socket.emit('request_data_60_host', {ip})
    socket.emit('request_data_12h_host', {ip})
    socket.emit('request_data_24h_host', {ip})
    socket.emit('request_data_protocols_host', {ip})

    socket.emit('request_data_sourceports_host', {ip})
    socket.emit('request_data_destports_host', {ip})

    socket.emit('request_top_sources_by_packet_count', {ip})
    socket.emit('request_top_destinations_by_packet_count', {ip})

    
    }


   
    useEffect(() => {
      fetchData()
      
      //Implementing the setInterval method
      const interval = setInterval(fetchData, 5000);

      //Clearing the interval
      return () => clearInterval(interval);
    }, []);


    socket.on('data_update_30_host', function(data) {
        
        console.log("ehere")
        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))

        setChart30Data({
          data:quantities,
          labels:timestamps
        })

      
    });

    socket.on('data_update_60_host', function(data) {
        

        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))
      
        setChart60Data({
          data:quantities,
          labels:timestamps
        })
    });

    
    socket.on('data_update_12h_host', function(data) {
        

        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))
      

        setChart12HData({
          data:quantities,
          labels:timestamps
        })
    });

    socket.on('data_update_24h_host', function(data) {
        

        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))
      
        setChart24HData({
          data:quantities,
          labels:timestamps
        })
    });



    socket.on('data_update_protocols_host', function(data) {
        

        data = JSON.parse(data)

        var protocols = data.map((d:any)=> (d.protocol))
        var quantities = data.map((d:any)=> (d.count))

        setChartprotocolsData({
          data:quantities,
          labels:protocols
        })
    });


    socket.on('data_update_sourceports_host', function(data) {
        

        data = JSON.parse(data)

        var ports = data.map((d:any)=> (d.port))
        var quantities = data.map((d:any)=> (d.count))

        
        setChartsourcePortsData({
          data:quantities,
          labels:ports
        })
    });


    socket.on('data_update_destports_host', function(data) {
        

        data = JSON.parse(data)

        var ports = data.map((d:any)=> (d.port))
        var quantities = data.map((d:any)=> (d.count))

        setChartDestPortsData({
          data:quantities,
          labels:ports
        })
    });


    socket.on("data_update_top_destinations_by_packet_count", function(data) {
        

      data = JSON.parse(data)

      var IPs = data.map((d:any)=> (d.dst_ip_address))
      var quantities = data.map((d:any)=> (d.count))

      setChartTopDestinationIPs({
        data:quantities,
        labels:IPs
      })
    });

    socket.on("data_update_top_sources_by_packet_count", function(data) {
        

      data = JSON.parse(data)

      var IPs = data.map((d:any)=> (d.src_ip_address))
      var quantities = data.map((d:any)=> (d.count))

      setChartTopSourceIPs({
        data:quantities,
        labels:IPs
      })
    });
    

  return (
    <>
    <SidebarWithHeader>
    
      
      <PanelHostGrid/>

      <SimpleGrid color="white" my="10" columns={1} spacing="6" >

    
      <Flex flexWrap={"wrap"}>
      <Heading w="100%" textAlign={"center"}></Heading>

      

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 30 minutes Host: {ip}</Text>
          <LineChart
            labels={chart30Data.labels}
            data={chart30Data.data}
          />
      </Center>

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 60 minutes Host: {ip}</Text>
          <LineChart
            labels={chart60Data.labels}
            data={chart60Data.data}
          />
      </Center>

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 12 hours Host: {ip}</Text>
          <LineChart
            labels={chart12HData.labels}
            data={chart12HData.data}
          />
      </Center>

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 24 hours Host: {ip}</Text>
          <LineChart
            labels={chart24HData.labels}
            data={chart24HData.data}
          />
      </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Protocols Host: {ip}</Text>
          <PieChart
            label={chartprotocolsData.labels}
            data={chartprotocolsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Protocols Host: {ip}</Text>
          <BarChart
              labels={chartprotocolsData.labels}
              data={chartprotocolsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Source Ports Host: {ip}</Text>
          <DoughnutChart
            label={chartsourcePortsData.labels}
            data={chartsourcePortsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Destination Ports Host: {ip}</Text>
          <DoughnutChart
            label={chartDestPortsData.labels}
            data={chartDestPortsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Top Captured Packet Destination IPs from host : {ip}</Text>
          <BarChart
              labels={chartTopDestinationIPs.labels}
              data={chartTopDestinationIPs.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
        <Text mb="2" textAlign={"center"} w="100%">Top Captured Packet Source IPs from host : {ip}</Text>
          <BarChart
              labels={chartTopSourceIPs.labels}
              data={chartTopSourceIPs.data}
          />
        </Center>
  
        
      </Flex>

      </SimpleGrid>
    </SidebarWithHeader>
    </>
  );
}