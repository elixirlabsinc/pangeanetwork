# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20180831033552) do

  create_table "co_ops", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.integer "phase_id", null: false
    t.boolean "is_active", null: false
    t.string "name", null: false
    t.datetime "start_date"
    t.datetime "end_date"
    t.string "location"
    t.integer "interest"
    t.integer "initial_balance"
    t.integer "expected_repayment"
    t.integer "current_balance"
  end

  create_table "loans", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.integer "user_id", null: false
    t.integer "balance", null: false
    t.integer "interest", null: false
    t.datetime "loan_start", null: false
    t.datetime "loan_end", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "phases", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string "phase_type"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "roles", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string "role_name", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "savings", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.integer "user_id", null: false
    t.integer "balance", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "transactions", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.integer "loan_id"
    t.integer "saving_id"
    t.integer "amount", null: false
    t.integer "previous_balance"
    t.integer "new_balance"
    t.integer "user_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string "aasm_state"
  end

  create_table "users", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string "email"
    t.string "encrypted_password"
    t.integer "role_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.integer "co_op_id"
    t.string "first_name"
    t.string "last_name"
    t.string "phone", null: false
  end

end
