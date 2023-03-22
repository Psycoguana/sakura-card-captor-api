const fs = require('fs');

exports.getAllCards = async (event, ctx) => {
	let data = fs.readFileSync(`${__dirname}/../card_info.json`, 'utf8');
	data = JSON.parse(data);

	let page = 1;
	let limit = 53;

	if (event.queryStringParameters?.page) {
		page = parseInt(event.queryStringParameters.page);
	}
	if (event.queryStringParameters?.limit) {
		limit = parseInt(event.queryStringParameters.limit);
	}

	const startIndex = (page - 1) * limit;
	const endIndex = page * limit;

	data = data.slice(startIndex, endIndex);

	return {
		statusCode: 200,
		headers: {
			'Access-Control-Allow-Origin': '*', // Required for CORS support to work
		},
		body: JSON.stringify(data),
	};
};

exports.getCard = async (event, ctx) => {
	const cardId = parseInt(event.queryStringParameters?.id);
	console.log(JSON.stringify('cardId'));

	console.log(JSON.stringify(cardId));
	if (!cardId) {
		return {
			statusCode: 400,
			headers: {
				'Access-Control-Allow-Origin': '*', // Required for CORS support to work
			},
			body: JSON.stringify({ message: 'Card ID not specified' }),
		};
	}

	let data = fs.readFileSync(`${__dirname}/../card_info.json`, 'utf8');
	data = JSON.parse(data);

	const card = data.find((card) => card.id === cardId);

	if (card === undefined) {
		return {
			statusCode: 404,
			headers: {
				'Access-Control-Allow-Origin': '*', // Required for CORS support to work
			},
			body: JSON.stringify({ message: 'ID not found' }),
		};
	}

	return {
		statusCode: 200,
		headers: {
			'Access-Control-Allow-Origin': '*', // Required for CORS support to work
		},
		body: JSON.stringify(card),
	};
};
