//**In Progress**

const {Client} = require('pg')

const client = new Client({
	host: 
	user: 
	port: 
	password:
	database: 
})

client.connect();

client.query('Select * from test_table1', (err,res)=>{
	if(err){
		console.log(res.rows);
	} else {
		console.log(err.message);
	}
	client.end;
})
