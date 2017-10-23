class UsersArtifactsJoinTable < ActiveRecord::Migration
  def change
    create_join_table :users, :artifacts do |t|
    	t.index :user_id
    	t.index :artifact_id
    end
  end
end
