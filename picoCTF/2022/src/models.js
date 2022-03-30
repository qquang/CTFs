const { Sequelize, Model, DataTypes } = require('sequelize');

const sequelize = new Sequelize({
	dialect: 'sqlite',
	storage: 'database.sqlite3'
});

class User extends Model {}

User.init({
	username: { type: DataTypes.STRING, unique: true },
	password: DataTypes.STRING,
}, { sequelize, modelName: 'user' });

class Note extends Model {}

Note.init({
	title: DataTypes.STRING,
	content: DataTypes.STRING,
}, { sequelize, modelName: 'note' });

User.hasMany(Note, { as: 'notes' });

Note.belongsTo(User, {
	foreignKey: 'userId',
	as: 'user'
});

sequelize.sync();

module.exports = { User, Note }