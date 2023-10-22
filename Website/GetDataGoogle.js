const mainrequest = async (city) => {
    const response = await axios.get(`http://localhost:5000?city=${city}`);

    return response.data;

}