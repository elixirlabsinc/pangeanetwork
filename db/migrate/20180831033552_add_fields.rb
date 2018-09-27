class AddFields < ActiveRecord::Migration[5.1]
  def change
    create_table :users do |t|
      t.string   :email
      t.string   :encrypted_password
      t.integer  :role_id
      t.datetime :created_at
      t.datetime :updated_at
      t.integer  :co_op_id
      t.string   :first_name
      t.string   :last_name
      t.string   :phone, null: false
    end

    create_table :roles do |t|
      t.string   :role_name, null: false
      t.datetime :created_at
      t.datetime :updated_at
    end

    create_table :co_ops do |t|
      t.integer :phase_id, null: false
      t.boolean :is_active, null: false
      t.string :name, null: false
      t.datetime :start_date
      t.datetime :end_date
      t.string :location
      t.integer :interest
      t.integer :initial_balance
      t.integer :expected_repayment
      t.integer :current_balance
    end

    create_table :phases do |t|
      t.string :phase_type
      t.datetime :created_at
      t.datetime :updated_at
    end

    create_table :loans do |t|
      t.integer :user_id, null: false
      t.integer :balance, null: false
      t.integer :interest, null: false
      t.datetime :loan_start, null: false
      t.datetime :loan_end, null: false
      t.datetime :created_at
      t.datetime :updated_at
    end

    create_table :savings do |t|
      t.integer :user_id, null: false
      t.integer :balance, null: false
      t.datetime :created_at
      t.datetime :updated_at
    end

    create_table :transactions do |t|
      t.integer :loan_id
      t.integer :saving_id
      t.integer :amount, null: false
      t.integer :previous_balance
      t.integer :new_balance
      t.integer :user_id, null: false
      t.datetime :created_at
      t.datetime :updated_at
      t.string   :aasm_state
    end
  end
end
